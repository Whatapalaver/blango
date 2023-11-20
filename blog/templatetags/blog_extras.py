from django import template
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from django.utils import timezone
from blog.models import Post

user_model = get_user_model()

register = template.Library()

@register.filter
def author_details(author, current_user=None):
  if not isinstance(author, user_model):
        # return empty string as safe default
        return ""
  if author == current_user:
        return format_html("<strong>me</strong>")
  if author.first_name and author.last_name:
    name =  f"{author.first_name} {author.last_name}"
  else:
    name = f"{author.username}"

  if author.email:
    # format_html - each argument is automatically escaped before being interpolated
    prefix = format_html('<a href="mailto:{}">', author.email)
    suffix = format_html("</a>")
  else:
    prefix = ""
    suffix = ""

  return format_html('{}{}{}', prefix, name, suffix)

# redoing the author_details_filter as a tag which has access to the context
@register.simple_tag(takes_context=True)
def author_details_tag(context):
  request = context["request"]
  current_user = request.user
  post = context["post"]
  author = post.author

  if author == current_user:
        return format_html("<strong>me</strong>")
  if author.first_name and author.last_name:
    name =  f"{author.first_name} {author.last_name}"
  else:
    name = f"{author.username}"

  if author.email:
    # format_html - each argument is automatically escaped before being interpolated
    prefix = format_html('<a href="mailto:{}">', author.email)
    suffix = format_html("</a>")
  else:
    prefix = ""
    suffix = ""

  return format_html('{}{}{}', prefix, name, suffix)

@register.simple_tag
def row(extra_classes=""):
    return format_html('<div class="row {}">', extra_classes)


@register.simple_tag
def endrow():
    return format_html("</div>")

@register.simple_tag
def col(extra_classes=""):
    return format_html('<div class="col {}">', extra_classes)


@register.simple_tag
def endcol():
    return format_html("</div>")

@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
  posts = Post.objects.filter(published_at__lte=timezone.now()).exclude(pk=post.pk).order_by("published_at")
  return {"posts": posts[:5], "title": "Recent Posts"}