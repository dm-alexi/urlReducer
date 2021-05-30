window.onload = () => {

    const input = document.querySelector(".input_text");
    const button = document.querySelector(".btn");
    const output = document.querySelector(".short_url");

    output.addEventListener('click',() => {
        navigator.clipboard.writeText(output.firstElementChild.innerText)
        .then(() => {
            output.lastElementChild.classList.remove('hidden');
        })
        .catch(err => {
            console.log('Something went wrong', err);
        });
    });

    button.addEventListener('click', (event) => {
        fetch('/api/v0', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 'url': input.value })
        }).then((resp) => {
            return resp.text();
        }).then((result) => {
            output.firstElementChild.innerText = result;
            output.lastElementChild.classList.add('hidden');
            output.classList.remove("hidden");
        });
    });
};