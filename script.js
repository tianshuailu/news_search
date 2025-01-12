// script.js

const button = document.getElementById('submit_button');
const loadingIndicator = document.getElementById("loading");
const responseDiv = document.getElementById('response');
const newsListDiv = document.getElementById("news_list");

button.addEventListener('click', async () => {
    const textInput = document.getElementById('user_input').value;

    newsListDiv.innerHTML = "";
    loadingIndicator.style.display = "block";

    if (!textInput) {
        responseDiv.innerHTML = `<p class="text-warning">Please enter some text!</p>`;
        return;
    }

    try {
        //TODO: change the url to the server url later
        const response = await fetch('http://127.0.0.1:8000/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: textInput }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        // Hide the loading indicator
        loadingIndicator.style.display = "none";

        articles = data.articles;

        responseDiv.innerHTML = `<p class="text-success">Here is a summary of the news articles on this topic: ${data.summary}</p>`;

        if (articles.length === 0) {
            newsListDiv.innerHTML = "<p>No articles found.</p>";
        } else {
            articles.forEach((article, index) => {
                const row = `
                    <a href="${article.url}" class="list-group-item list-group-item-action d-flex gap-3 py-3" aria-current="true">
                        <div class="d-flex gap-2 w-100 justify-content-between">
                            <div>
                                <h6 class="mb-0">${article.title}</h6>
                            </div>
                            <small class="opacity-50 text-nowrap">${article.published_at}</small>
                        </div>
                    </a>
                `;
                newsListDiv.insertAdjacentHTML("beforeend", row);
            });
        }

    } catch (error) {
        // Hide the loading indicator and show an error message
        loadingIndicator.style.display = "none";
        responseDiv.innerHTML = `<p class="text-danger">Error: ${error.message}</p>`;
    }
});
