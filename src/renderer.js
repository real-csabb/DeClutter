const main = () => {
    fetch('top-bar.html')
        .then(response => response.text())
        .then(templateHTML => {
            // Create temporary container
            let container = document.createElement('div');
            container.innerHTML = templateHTML;

            // Find template element inside container
            const topBarElement = container.querySelector('#topbar');

            // Import the template into the document
            const topBar = document.importNode(topBarElement.content, true);

            // Append template to the desired location within the document
            const newContainer = document.querySelector('#topbar-container');
            newContainer.appendChild(topBar);

            // Handle username
            fillInUsername('Time Lord Victorious');

            handleSearch();
            handleDropdown();
        })
        .catch(error => {
            console.error('Error loading template: ', error);
        });
    fetch('footer.html')
        .then(response => response.text())
        .then(templateHTML => {
            // Create temporary container
            let container = document.createElement('div');
            container.innerHTML = templateHTML;

            // Find template element inside container
            const footerElement = container.querySelector('#footer');

            // Import the template into the document
            const footer = document.importNode(footerElement.content, true);

            // Append template to the desired location within the document
            const newContainer = document.getElementById('footer-container');
            newContainer.appendChild(footer);

            // // Handle username
            // fillInUsername('Chris Sabb');
        })
        .catch(error => {
            console.error('Error loading template: ', error);
        });

    //const polisciJson = require('./polisci.json');

    awaitServerStart().then(
        response => response.text()
    ).then(
        responseText => {
            console.log(responseText)
            processJSON();
        }
    );
};

const awaitServerStart = async () => {
    return new Promise((resolve, reject) => {
        const checkStatus = () => {
            fetch('http://127.0.0.1:3000/')
                .then(response => {
                    if (response.ok) {
                        console.log('Server is ready');
                        resolve(response); // Resolve the promise once server is ready
                    } else {
                        console.log('Server is not ready yet, retrying...');
                        setTimeout(checkStatus, 100); // Retry after 100 milliseconds
                    }
                }).catch(error => {
                //console.error('Error checking server status:', error);
                setTimeout(checkStatus, 100);
            });
        };

        // Start checking server status
        checkStatus();
    });
};

// Gets json data from the database and acts appropriately
const processJSON = () => {
    processFiles();
    processCategories();
};

const processCategories = () => {
    fetch('http://127.0.0.1:3000/categories').then(response => response.json())
        .then(json => {
            const categoriesHolder = document.getElementById('categories-holder');
            categoriesHolder.innerHTML = '';

            for (let i = 0; i < json.length; i++) {
                const categoryElement = document.createElement('a');
                categoryElement.appendChild(document.createElement('a'));
                fillInCategory(categoryElement, json[i]);
                categoryElement.href = `tab.html?id=${i + 1}&name=${categoryElement.innerText}`;
                categoriesHolder.appendChild(categoryElement);
            }
        })
};

// Gets files and adds them to the UI
const processFiles = () => {
    let options = {
        method: 'GET'
    }

    let apiEndpoint = 'files';

    if (document.title === 'tab') {
        const urlParams = new URLSearchParams(window.location.search);
        const id = urlParams.get('id');
        const name = urlParams.get('name');
        console.log(id);
        console.log(name);
        const nameElement = document.getElementById('name');
        nameElement.innerText = name;

        options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' // Specify that the data being sent is JSON
            },
            body: JSON.stringify(id)
        };

        apiEndpoint = 'files-by-category';
    }

    fetch(`http://127.0.0.1:3000/${apiEndpoint}`, options).then(response => response.json())
        .then(handleFileJson);
};

const handleFileJson = json => {
    const rowLength = 4; // Number of files in a row

    const fileHolder = document.querySelector('#files-holder');
    // Clear all
    fileHolder.innerHTML = '';

    // Fetch file template
    fetch('file.html')
        .then(response => response.text())
        .then(templateHTML => {
            // Create temporary container
            let container = document.createElement('div');
            container.innerHTML = templateHTML;

            // Find template element inside container
            const fileElement = container.querySelector('#file');

            // Import the template into the document
            return document.importNode(fileElement.content, true);
        }).then(file => {
        for (let i = 0; i < json.length; i++) {
            if (i % rowLength === 0) {
                const row = document.createElement('div');
                row.className = 'box-row';
                fileHolder.appendChild(row);
            }

            fillInFile(file, json[i]);
            const newFile = file.cloneNode(true);
            newFile.id = i;
            fileHolder.lastElementChild.appendChild(newFile);
        }
    });
};

// Retrieves search input from the user
const handleSearch = () => {
    // Default text for dropdown is an empty string
    handleDropdown();

    const searchInput = document.querySelector('.nav-search-input');
    console.log("SEARCH VALUE:" + searchInput.value.charCodeAt(0));

    searchInput.addEventListener('input', () => {
        const text = searchInput.value;
        handleDropdown();
        console.log('TEXT: ' + text);
        // Get
    });

    searchInput.addEventListener('keydown', event => {
        //event.preventDefault();

        if (event.key === 'Enter') {
            getFilesByKeyword(searchInput.value);
        }
    });

    const searchIcon = document.querySelector('.nav-search-icon');

    searchIcon.addEventListener('click', event => {
        event.preventDefault();
        getFilesByKeyword(searchInput.value);
    });
};

const handleDropdown = () => {
    const dropdown = document.querySelector('.dropdown-content');
    const searchInput = document.querySelector('.nav-search-input');
    dropdown.innerHTML = '';
    dropdown.style.display = searchInput.value === '' ? 'none' : 'block';

    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Specify that the data being sent is JSON
        },
        body: JSON.stringify(searchInput.value)
    };

    console.log(options);

    fetch('http://127.0.0.1:3000/dropdown', options).then(response => response.json())
        .then(json => {
            for (const keyword of json) {
                const listElem = document.createElement("li");
                listElem.innerText = keyword;
                listElem.addEventListener('click', event => {
                    event.preventDefault();
                    getFilesByKeyword(keyword);
                });
                dropdown.appendChild(listElem);
            }
        });
};

const getFilesByKeyword = keyword => {
    const options = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Specify that the data being sent is JSON
        },
        body: JSON.stringify(keyword)
    };

    fetch('http://127.0.0.1:3000/search', options)
        .then(response => response.json())
        .then(handleFileJson);
};

// Replaces the inner text of all occurrences of the username class with a given username
const fillInUsername = username => {
    // Get all instances of username
    const usernamePlaceholders = document.getElementsByClassName('username');

    // Replace every one with the username
    for (const placeholder of usernamePlaceholders) {
        placeholder.innerText = username;
    }
};

// Replaces file inner HTML with desired HTML
const fillInFile = (file, json) => {
    const hoverSpan = file.querySelector('.onhover');
    hoverSpan.innerText = json.hoverText;

    const title = file.querySelector('.title');
    title.innerText = json.title;

    const image = file.querySelector('.image');
    image.src = json.imagePath;

    const link = file.querySelector('.link');
    link.href = json.imagePath;
};

const fillInCategory = (category, json) => {
    // Get top keyword for category
    category.innerText = json.name;
};
