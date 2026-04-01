from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.search import index
from wagtail.images.blocks import ImageChooserBlock

# --- Reusable Blocks ---

class HeroSlideBlock(blocks.StructBlock):
    tab_name = blocks.CharBlock(required=True, help_text="Text for the bottom tab")
    title = blocks.CharBlock(required=True)
    subtitle = blocks.TextBlock(required=True)
    cta_text = blocks.CharBlock(default="Get a Quote")
    image = ImageChooserBlock(required=True)

class FAQBlock(blocks.StructBlock):
    question = blocks.CharBlock(required=True)
    answer = blocks.TextBlock(required=True)

class TestimonialBlock(blocks.StructBlock):
    quote = blocks.TextBlock(required=True)
    author_name = blocks.CharBlock(required=True)
    author_company = blocks.CharBlock(required=False)
    image = ImageChooserBlock(required=True)

class InsightBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    description = blocks.TextBlock(required=True)
    link = blocks.PageChooserBlock(required=False)

# --- Service Blocks (Separated to keep Admin clean) ---

class ServiceBlock(blocks.StructBlock):
    """Simple version for the Home Page Grid"""
    title = blocks.CharBlock(required=True)
    short_benefit = blocks.CharBlock(required=True, help_text="Short sub-benefit description")
    description = blocks.TextBlock(required=True)
    icon = blocks.CharBlock(required=False, help_text="Lucide icon name")

class DetailedServiceBlock(blocks.StructBlock):
    """Detailed version for the Services Page Detail View"""
    title = blocks.CharBlock(required=True)
    short_benefit = blocks.CharBlock(required=True)
    description = blocks.TextBlock(required=True)
    icon = blocks.CharBlock(required=False)
    
    # Detail View Fields
    detail_image = ImageChooserBlock(required=True, help_text="Background for the detail hero")
    secondary_image = ImageChooserBlock(required=True, help_text="Sidebar square image")
    process_1 = blocks.TextBlock(required=True)
    process_2 = blocks.TextBlock(required=True)
    tags = blocks.ListBlock(blocks.CharBlock(), help_text="Technical tags")

# --- Page Models ---

class HomePage(Page):
    # Hero Section
    hero_slides = StreamField([('slide', HeroSlideBlock())], use_json_field=True, blank=True, max_num=4)

    # Animated Headline
    animated_headline_intro = models.CharField(max_length=255, default="Agile ICT Solutions helps enterprises")
    animated_word_1 = models.CharField(max_length=50, default="modernize")
    animated_subword_1 = models.CharField(max_length=50, default="infrastructure")
    animated_word_2 = models.CharField(max_length=50, default="optimize")
    animated_subword_2 = models.CharField(max_length=50, default="operations")
    animated_word_3 = models.CharField(max_length=50, default="secure")
    animated_subword_3 = models.CharField(max_length=50, default="networks")
    animated_conjunction = models.CharField(max_length=50, default="and")
    animated_headline_outro = models.CharField(max_length=255, default="so they stay ahead in a fast-changing world.")

    # Fixed Banner
    banner_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    banner_title = models.CharField(max_length=255, default="Architecting PNG's Digital Future")
    banner_description = models.TextField(default="We bridge the gap between global technologies and local needs.")
    banner_cta_text = models.CharField(max_length=50, default="Who We Are")
    banner_cta_link = models.ForeignKey('wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text="About page link")

    # Expertise Section
    expertise_title = models.CharField(max_length=255, default="Integrated ICT Solutions")
    expertise_subtitle = models.TextField(default="Delivering excellence across your digital landscape.")
    service_card_cta = models.CharField(max_length=50, default="Learn More")
    promo_card_text = models.CharField(max_length=50, default="Explore Solutions")
    promo_card_link = models.ForeignKey('wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+', help_text="Services page link")

    # Services (Simple Block)
    services = StreamField([('service', ServiceBlock())], use_json_field=True, blank=True)

    # Bottom CTA
    bottom_cta_title = models.CharField(max_length=255, default="Tailored Solutions for Your Enterprise")
    bottom_cta_description = models.TextField(default="Partner with our engineering team.")
    bottom_cta_button_text = models.CharField(max_length=50, default="Get a free quote")
    bottom_cta_link = models.ForeignKey('wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    # Partners
    vendor_label = models.CharField(max_length=255, default="Strategic Partners & Vendors")

    # FAQs
    faq_section_title = models.CharField(max_length=255, default="Frequently Asked Questions")
    faqs = StreamField([('faq', FAQBlock())], use_json_field=True, blank=True)
    faq_cta_text = models.CharField(max_length=50, default="Explore All FAQ's")
    faq_cta_link = models.ForeignKey('wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    # Testimonials
    testimonial_subheading = models.CharField(max_length=100, default="Enterprise")
    testimonial_heading_line_1 = models.CharField(max_length=100, default="Success")
    testimonial_heading_line_2 = models.CharField(max_length=100, default="Stories")
    testimonials = StreamField([('testimonial', TestimonialBlock())], use_json_field=True, blank=True)

    # Insights
    insights_subheading = models.CharField(max_length=100, default="2026 Horizon")
    insights_heading = models.CharField(max_length=100, default="Industry Insights")
    insights_cta_text = models.CharField(max_length=50, default="View All Insights")
    insights_cta_link = models.ForeignKey('wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    insights = StreamField([('insight', InsightBlock())], use_json_field=True, blank=True)

    # Careers
    careers_image = models.ForeignKey('wagtailimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    careers_heading = models.CharField(max_length=255, default="Drive your career forward. Fast.")
    careers_cta_text = models.CharField(max_length=50, default="Browse job listings")
    careers_cta_link = models.ForeignKey('wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    # Final CTA
    final_cta_subheading = models.CharField(max_length=100, default="Infrastructure Deployment")
    final_cta_heading = models.CharField(max_length=255, default="Architecting the future.")
    final_cta_box_heading = models.CharField(max_length=255, default="Let's build it.")
    final_cta_box_hover_text = models.CharField(max_length=100, default="Engage our team")
    final_cta_link = models.ForeignKey('wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    content_panels = Page.content_panels + [
        FieldPanel('hero_slides', heading="Hero Slider Settings"),
        MultiFieldPanel([
            FieldPanel('animated_headline_intro'),
            FieldPanel('animated_word_1'), FieldPanel('animated_subword_1'),
            FieldPanel('animated_word_2'), FieldPanel('animated_subword_2'),
            FieldPanel('animated_word_3'), FieldPanel('animated_subword_3'),
            FieldPanel('animated_conjunction'),
            FieldPanel('animated_headline_outro'),
        ], heading="Animated Headline Section"),
        MultiFieldPanel([
            FieldPanel('banner_image'), FieldPanel('banner_title'),
            FieldPanel('banner_description'), FieldPanel('banner_cta_text'),
            FieldPanel('banner_cta_link'),
        ], heading="Fixed Banner Section"),
        MultiFieldPanel([
            FieldPanel('expertise_title'), FieldPanel('expertise_subtitle'),
            FieldPanel('service_card_cta'), FieldPanel('promo_card_text'),
            FieldPanel('promo_card_link'),
        ], heading="Expertise / Services Section Settings"),
        MultiFieldPanel([FieldPanel('vendor_label')], heading="Partner Marquee Settings"),
        FieldPanel('services'),
        MultiFieldPanel([
            FieldPanel('bottom_cta_title'), FieldPanel('bottom_cta_description'),
            FieldPanel('bottom_cta_button_text'), FieldPanel('bottom_cta_link'),
        ], heading="Bottom Call to Action Section"),
        MultiFieldPanel([
            FieldPanel('faq_section_title'), FieldPanel('faqs'),
            FieldPanel('faq_cta_text'), FieldPanel('faq_cta_link'),
        ], heading="FAQ Section"),
        MultiFieldPanel([
            FieldPanel('testimonial_subheading'), FieldPanel('testimonial_heading_line_1'),
            FieldPanel('testimonial_heading_line_2'), FieldPanel('testimonials'),
        ], heading="Testimonial Section Settings"),
        MultiFieldPanel([
            FieldPanel('insights_subheading'), FieldPanel('insights_heading'),
            FieldPanel('insights_cta_text'), FieldPanel('insights_cta_link'),
            FieldPanel('insights'),
        ], heading="Insights Section Settings"),
        MultiFieldPanel([
            FieldPanel('careers_image'), FieldPanel('careers_heading'),
            FieldPanel('careers_cta_text'), FieldPanel('careers_cta_link'),
        ], heading="Careers Section Settings"),
        MultiFieldPanel([
            FieldPanel('final_cta_subheading'), FieldPanel('final_cta_heading'),
            FieldPanel('final_cta_box_heading'), FieldPanel('final_cta_box_hover_text'),
            FieldPanel('final_cta_link'),
        ], heading="Final Call to Action Settings"),
    ]

class ServicesPage(Page):
    # Hero Section
    hero_line_1 = models.CharField(max_length=255, default="Digital")
    hero_line_2_outline = models.CharField(max_length=255, default="Infrastructure")
    hero_line_3 = models.CharField(max_length=255, default="Evolution")

    # Services Grid (Detailed Block)
    services = StreamField([('service', DetailedServiceBlock())], use_json_field=True, blank=True)

    # Bottom CTA
    cta_title = models.CharField(max_length=255, blank=True, help_text="e.g., 'Ready to Initiate?'")
    cta_button_text = models.CharField(max_length=50, blank=True, default="Consultation")
    cta_link = models.ForeignKey('wagtailcore.Page', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_line_1'),
            FieldPanel('hero_line_2_outline'),
            FieldPanel('hero_line_3'),
        ], heading="Hero Section"),
        FieldPanel('services', heading="Detailed Services List"),
        MultiFieldPanel([
            FieldPanel('cta_title'),
            FieldPanel('cta_button_text'),
            FieldPanel('cta_link'),
        ], heading="Bottom Call to Action"),
    ]