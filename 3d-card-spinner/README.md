
# 3D Card Spinner

A 3D card spinner built on top of Flask that showcases rotating images with a smooth 3D animation effect. The application uses HTML, CSS, and Flask to deliver an interactive, visually appealing experience.

## Live Demo

You can see a live demo of the application here: [3D Card Spinner Demo](https://claudezion.pythonanywhere.com/spinner)

## Features

- 3D rotating card spinner with customizable images.
- Flask backend to serve static files and run the application.
- Smooth animation and responsive design using pure CSS.

## Installation

To run this project locally:

1. Clone the repository.

   ```bash
   git clone https://github.com/your-username/3d-card-spinner-flask.git
   cd 3d-card-spinner-flask
   ```

2. Set up a virtual environment and install dependencies.

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Place your images in the `/static/` folder with filenames `image1.jpg`, `image2.jpg`, ..., `image10.jpg`. Adjust the paths in `index.html` if needed.

4. Run the Flask application.

   ```bash
   flask run
   ```

5. Open `http://127.0.0.1:5000/spinner` in your browser to view the spinner.

## Project Structure

```
.
├── app.py            # Flask application file
├── templates/
│   └── index.html    # Main HTML for the spinner
├── static/
│   ├── style.css     # CSS for styling and animation
│   ├── image1.jpg    # Example images for the spinner
│   └── image2.jpg
└── requirements.txt  # Dependencies for the Flask app
```

## Customization

### Changing the Number of Cards

Update the `--quantity` variable in the HTML's `.spinner` class and add or remove `.card` elements:

```html
<div class="spinner" style="--quantity: 10">
  <!-- Add or remove card elements here -->
</div>
```

### Adjusting Animation Speed

Modify the `animation` duration in the CSS to control the speed:

```css
@keyframes spin {
  from {
    transform: perspective(1000px) rotateX(-16deg) rotateY(0deg);
  }
  to {
    transform: perspective(1000px) rotateX(-16deg) rotateY(360deg);
  }
}
```

Change `20s` to your desired value for the `animation` property.

### Changing the Images

Replace the `src` in the `.card img` tags with your own images in the `/static/` directory.

```html
<img src="/static/image1.jpg" alt="" />
```

## License

This project is licensed under the MIT License.
```

This version includes Flask-specific setup instructions and highlights the live demo link.
