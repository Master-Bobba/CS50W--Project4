document.addEventListener('DOMContentLoaded', function(){

    like_button = document.querySelectorAll('button').forEach(button => {
        button.onclick = function() {
            button.innerHTML = (button.innerHTML === "Like") ? button.innerHTML="Unlike": button.innerHTML = 'Like';
            
            likes = document.querySelector(`#likes-count-${this.dataset.post}`);
            console.log(`${likes}`);
            if (button.innerHTML === "Like")  {  
                likes.innerHTML = parseInt(likes.innerHTML) - 1;
                fetch('/like/' + this.dataset.post, {
                    method: 'PUT',
                    body: JSON.stringify({
                        unlike: this.dataset.post
                    })
                })
            } else {
                likes.innerHTML = parseInt(likes.innerHTML) + 1;
                fetch('/like/' + this.dataset.post, {
                    method: 'PUT',
                    body: JSON.stringify({
                        like: this.dataset.post
                    })
                })
            }

            
        }
    });


});