import re
import json
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.response import TemplateResponse
from django.utils.html import strip_tags
from wagtail.models import Page, Locale
from django.http import JsonResponse

def extract_page_text(page):
    """Helper function to pull text out of our custom Wagtail fields"""
    text_parts = []
    
    # Check standard text fields
    if hasattr(page, 'hero_subtitle') and page.hero_subtitle:
        text_parts.append(strip_tags(str(page.hero_subtitle)))
    if hasattr(page, 'expertise_subtitle') and page.expertise_subtitle:
        text_parts.append(strip_tags(str(page.expertise_subtitle)))
        
    # Check inside the 'services' StreamField
    if hasattr(page, 'services') and page.services:
        for block in page.services:
            if 'title' in block.value:
                text_parts.append(strip_tags(str(block.value['title'])))
            if 'description' in block.value:
                text_parts.append(strip_tags(str(block.value['description'])))
                
    return " ".join(text_parts)

def get_context_snippet(text, query, length=150):
    """Finds the query in the text and returns a snippet around it"""
    if not query or not text: return ""
    text = " ".join(text.split()) # Normalize whitespace
    
    # Find the keyword ignoring case
    match = re.search(re.escape(query), text, re.IGNORECASE)
    if match:
        start = max(0, match.start() - (length // 2))
        end = min(len(text), match.end() + (length // 2))
        snippet = text[start:end]
        if start > 0: snippet = "..." + snippet
        if end < len(text): snippet = snippet + "..."
        return snippet
    return ""

def search(request):
    search_query = request.GET.get('query', None)
    page = request.GET.get('page', 1)
    active_locale = Locale.get_active()

    if search_query:
        search_results = Page.objects.live().filter(locale=active_locale).search(search_query)
    else:
        search_results = Page.objects.none()

    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    # Attach the dynamic snippet to each result
    for result in search_results:
        specific_page = result.specific
        full_text = extract_page_text(specific_page)
        snippet = get_context_snippet(full_text, search_query)
        
        # If we found the word in the text, use it. Otherwise fallback to Wagtail's search_description
        if snippet:
            result.context_snippet = snippet
        else:
            result.context_snippet = result.search_description or "Click to view this page's content."

    return TemplateResponse(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
    })



import os
from google import genai
from django.http import JsonResponse
from wagtail.models import Page, Locale
# ... (ensure your extract_page_text function is still here) ...

def ai_search_summary(request):
    """
    Async endpoint that takes a query, reads the top search results, 
    and asks Gemini to summarize them.
    """
    query = request.GET.get('query', '')
    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)

    active_locale = Locale.get_active()
    
    # Get the top 3 results to feed to the AI
    top_results = Page.objects.live().filter(locale=active_locale).search(query)[:3]
    
    if not top_results:
        return JsonResponse({'summary': None})

    # Extract the text from these top pages
    context_text = []
    for result in top_results:
        text = extract_page_text(result.specific)
        context_text.append(f"Source: {result.title}\nContent: {text}")
        
    combined_context = "\n\n".join(context_text)

    # ==========================================
    # ACTUAL AI INTEGRATION
    # ==========================================
    
    # IMPORTANT: In production, NEVER hardcode your API key. 
    # Use environment variables or a .env file.
    # For quick testing, you can temporarily paste it below.
    api_key = os.environ.get("GEMINI_API_KEY", "AIzaSyA-ZHlUVXD8U5Lq4hOLdyzAsMHQ4DN8MM0")
    
    if api_key == "PASTE_YOUR_API_KEY_HERE":
        return JsonResponse({'summary': "Please configure your GEMINI_API_KEY in views.py to see the live AI response."})

    try:
        # Initialize the Gemini Client
        client = genai.Client(api_key=api_key)
        
        # The System Prompt: Telling the AI exactly how to behave
        prompt = f"""
        You are an intelligent, professional assistant for the website 'agile ICT solutions'.
        A user searched for the term: '{query}'.
        
        Based ONLY on the following website excerpts, write a concise, 2-3 sentence summary 
        explaining how this relates to our services or what the user can find on our site.
        Do not use external knowledge. Do not use markdown formatting (like asterisks or bolding).
        If the excerpts do not contain enough information, briefly state that we provide comprehensive 
        ICT solutions and encourage them to contact us for specific details.
        
        Website Excerpts:
        {combined_context}
        """

        # Call the Gemini 2.5 Flash model (it is incredibly fast for this type of task)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        return JsonResponse({
            'summary': response.text
        })
        
    except Exception as e:
        # If the API fails (network error, quota, etc.), fail gracefully
        print(f"AI Generation Error: {e}")
        return JsonResponse({
            'summary': "We are currently experiencing high traffic. Please view the standard search results below for your query."
        })