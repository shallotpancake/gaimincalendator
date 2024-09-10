def extract_category_and_title_from_href(href):
    # Extracts the category and the title from the href
    parts = href.split('/')
    if len(parts) >= 4 and parts[2] == 'Special:Stream':
        category = parts[3]  # The service category (e.g., 'twitch', 'youtube')
        title = '/'.join(parts[4:])  # The rest of the href (stream title)
        return category, title
    return 'unknown', href  # Default category and title
