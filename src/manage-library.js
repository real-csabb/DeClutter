// Handle the dialog here
const openFileDialog = event => {
    event.preventDefault(); // Prevent the default behavior of the button click event
    window.ipc.chooseFiles({
        properties: ['openFile', 'multiSelections'],
        filters: [
            {
                name: 'Images or PDFs',
                extensions: ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'tif', 'svg', 'webp', 'ico', 'raw', 'pdf']
            }
        ]
    }).then(result => {
        // Post to database
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json' // Specify that the data being sent is JSON
            },
            body: JSON.stringify(result.filePaths)
        };

        // Add files to currently selected box
        const currentlySelectedDialog = document.getElementById('currently-selected');
        currentlySelectedDialog.value = result.filePaths.join('\n\n');

        fetch('http://127.0.0.1:3000/add-files', options).then(response => console.log(response)).then(
            json => alert('json uploaded' + json)
        );
    })
        .catch(err => console.log(err));
};

// Saves added files to the database
const saveFiles = event => {
    event.preventDefault();
    fetch('http://127.0.0.1:3000/save-files').then(response => {
        console.log(response);
        const currentlySelectedDialog = document.getElementById('currently-selected');
        const recentlyAddedDialog = document.getElementById('recently-added');
        recentlyAddedDialog.value = currentlySelectedDialog.value;
        currentlySelectedDialog.value = null;
    })
        .catch(err => console.log(err));
};
