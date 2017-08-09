
def truncate_string(text, max_length=50):
    return (text[:max_length - 3] + '...') if len(text) > max_length else text
