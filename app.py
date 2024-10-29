def fetch_images(description, num_images=3):
    """
    Fetch images from Unsplash based on a description.
    """
    # Keywords extraction (example logic)
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(description)
    keywords = [word for word in words if word.isalpha() and word.lower() not in stop_words]
    search_query = ", ".join(keywords[:5])

    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": search_query,
        "per_page": num_images,
        "client_id": UNSPLASH_ACCESS_KEY,
        "orientation": "landscape"
    }
    response = requests.get(url, params=params)
    
    # Collect image URLs if the request is successful
    image_urls = [result['urls']['regular'] for result in response.json().get('results', [])] if response.status_code == 200 else []
    return image_urls


def generate_prototype(description, logo_url=None, functionality=False):
    """
    Generates a web prototype using Generative AI based on the provided description.
    Optional parameters include a logo URL and a toggle for adding interactive functionality.
    """
    # Fetch related images from Unsplash
    image_urls = fetch_images(description)
    images_html = "".join([f'<img src="{url}" alt="Image related to {description}" style="width:100%; height:auto;">' for url in image_urls])

    # Prompt for the generative AI to create HTML, CSS, and JavaScript code
    prompt = f"""
    Generate HTML, CSS, and JavaScript code for: {description}.
    Requirements: Responsive layout, Flexbox/CSS Grid, Images: {images_html}.
    """
    if logo_url:
        prompt += f"Use this logo: {logo_url}."
    if functionality:
        prompt += " Add interactive JavaScript elements."

    # Start a session with Google Generative AI and generate the response
    chat_session = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config={
            "temperature": 1.6,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        },
    ).start_chat(history=[{"role": "user", "parts": [prompt]}])

    # Send message to generate the prototype
    response = chat_session.send_message("Generate the web prototype")
    return response.text
