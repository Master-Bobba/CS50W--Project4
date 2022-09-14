document.addEventListener('DOMContentLoaded', function(){

    like_button = document.querySelectorAll('.like-button').forEach(button => {
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

    edit_buttons = document.querySelectorAll('.edit-button').forEach(edit_button => {
        edit_button.onclick = function() {
            content=document.querySelector(`#post-content-${this.dataset.edit}`);
            
            console.log(`${this.dataset.edit}`);
            // Create the text area element with the post content
            const text_area = document.createElement("TEXTAREA");
            
            text_area.innerHTML = content.innerHTML;
            text_area.cols = 75;
            text_area.rows = 3;
            text_area.id = this.dataset.edit;
            

            // Submit the form
            text_area.addEventListener('keypress', function(event) {
                if (event.which === 13){
                    content.innerHTML = text_area.value;
                    console.log(`${text_area.id}`);
                    fetch('/edit/' + text_area.id, {
                        method: 'PUT',
                        body: JSON.stringify({
                            edit: text_area.value
                        })
                    })
                }

            });

            content.innerHTML = "";
            content.appendChild(text_area);
        }
    });

});