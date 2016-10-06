from django import template

register = template.Library()

@register.filter
def activate(title, text):
	if text in title:
		return 'active'
	return ''

@register.filter
def set_title(title):
	return ' - '.join(title)

@register.filter(is_safe = True)
def	print_accordion(products):
	tmp = ""
	html = ""
	for i, product in enumerate(products):
		if product.category.entity.name not in tmp:
			tmp = product.category.entity.name
			if i:
				html += '</tbody></table></div>'
			html += '<div class = "title"><i class = "dropdown icon"></i>' + product.category.entity.name + '</div><div class = "content"><table class = "ui basic table"><thead><tr><th>Nom</th><th>Prix</th></tr></thead><tbody>'
		html += '<tr><td>' + product.name + '</td><td>' + str(product.price) + '</td></tr>'
	html += '</tbody></table></div>'
	return html	

@register.filter
def	addcss(field, css):
	return field.as_widget(attrs = {"class" : css})
