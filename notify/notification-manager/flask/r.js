const apiUrl = 'http://127.0.0.1:5000/selectedusers';

fetch(apiUrl)
.then(response => {
if (!response.ok) {
throw new Error('Network response was not ok ' + response.statusText);
}
return response.json();
})
.then(data => {
console.log(data);

})
.catch(error => {
console.error('Error fetching usernames:', error);
});
