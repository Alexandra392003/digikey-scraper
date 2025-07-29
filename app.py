from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route('/get_price', methods=['POST'])
def get_price():
    data = request.get_json()
    url = data.get("url") if data else None

    if not url:
        return jsonify({"error": "URL is missing"}), 400

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto(url, timeout=30000)
            page.wait_for_timeout(4000)  # așteaptă JS-ul să încarce
            # Selectorul pentru preț (poți adapta dacă se schimbă)
            price_locator = page.locator("td.MuiTableCell-alignRight span").first
            price = price_locator.text_content()
            browser.close()
            if price:
                return jsonify({"price": price.strip()})
            else:
                return jsonify({"error": "Price not found"}), 404
        except Exception as e:
            browser.close()
            return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
