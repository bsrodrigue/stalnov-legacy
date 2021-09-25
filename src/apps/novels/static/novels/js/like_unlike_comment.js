document.querySelector("#like-button").addEventListener("click", event => {
    event.preventDefault();
    let csrfTokenValue = document.querySelector('[name=csrfmiddlewaretoken]').value;
	let formData = new FormData();
	formData.append('chapter_id', document.querySelector("#likeForm-chapter_id").value)
    const request = new Request('{% url \'like_chapter\' %}', {
        method: 'POST',
        body: formData,
        headers: {'X-CSRFToken': csrfTokenValue}  
    });
	console.log(request);
	fetch(request)
	.then(response => response.json())
	.then(result => {
		console.log(result)
	})
});
