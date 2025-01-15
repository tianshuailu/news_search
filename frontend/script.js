// script.js

const button = document.getElementById('submit_button');
const loadingIndicator = document.getElementById("loading");
const responseDiv = document.getElementById('response');
const summaryDiv = document.getElementById('summary');
const newsListDiv = document.getElementById("news_list");
const searchInput = document.getElementById("user_input");

// Save user input to session storage whenever it changes
searchInput.addEventListener("input", () => {
    sessionStorage.setItem("searchInputValue", searchInput.value);
});

// Load saved user input, summary, and aricles on page load
document.addEventListener("DOMContentLoaded", () => {
    const savedInputValue = sessionStorage.getItem("searchInputValue");
    if (savedInputValue) {
        searchInput.value = savedInputValue;
    }

    const savedSummary = sessionStorage.getItem("summary");
    if (savedSummary) {
        summaryDiv.innerHTML = `<p class="lead mb-4">Here is a summary of the news articles on this topic:<br> ${savedSummary}</p>`;;
    }

    const savedArticles = sessionStorage.getItem("newsArticles");
    if (savedArticles) {
        const articles = JSON.parse(savedArticles);
        renderNews(articles);
    }
});

// Add event listener to the "Fetch News" button
button.addEventListener("click", fetchNews);

// Function to fetch news from the backend
async function fetchNews() {
    const textInput = searchInput.value;
    responseDiv.innerHTML = ""; // Clear any previous response
    summaryDiv.innerHTML = ""; // Clear any previous summary
    if (!textInput) {
        responseDiv.innerHTML = `<p class="text-warning">Please enter some text!</p>`;
        return;
    }

    // Clear the table and show the loading indicator
    newsListDiv.innerHTML = "";
    loadingIndicator.style.display = "block";

    try {
        //TODO: change the url to the server url later?
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

        // data: {"summary": summary, "keywords": keywords, "articles": result_list}
        const data = await response.json();
        articles = data.articles;

        // Hide the loading indicator
        loadingIndicator.style.display = "none";

        // Save articles to sessionStorage
        sessionStorage.setItem("newsArticles", JSON.stringify(articles));

        // Display the summary
        summaryDiv.innerHTML = `<p class="lead mb-4">Here is a summary of the news articles on this topic:<br> ${data.summary}</p>`;
        sessionStorage.setItem("summary", data.summary);

        // Render the articles in the table
        renderNews(articles);
    } catch (error) {
        // Hide the loading indicator and display an error
        loadingIndicator.style.display = "none";
        newsListDiv.innerHTML = `<tr><td colspan='3' class="text-danger">Error: ${error.message}</td></tr>`;
        console.error("Error fetching articles:", error);
    }
}

// Function to render news articles in the table
function renderNews(articles) {
    newsListDiv.innerHTML = ""; // Clear existing content
    if (articles.length === 0) {
        newsListDiv.innerHTML = "<tr><td colspan='3'>No articles found.</td></tr>";
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
}