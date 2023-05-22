function likeHandler(id, liked) {
  const boton = document.getElementById(`${id}`);

  
  if (liked === undefined) {
    liked = ""; 
  }

  let isLiked = liked.indexOf(id) >= 0;

  boton.classList.toggle('fa-thumbs-up', isLiked);
  boton.classList.toggle('fa-thumbs-down', !isLiked);

  fetch(isLiked ? `/deslike/${id}` : `/like/${id}`)
    .then(response => response.json)
    .then(result => {
      boton.classList.toggle("fa-thumbs-up", !isLiked);
      boton.classList.toggle("fa-thumbs-down", isLiked);
      isLiked = !isLiked;
     location.reload();
    });
}


const getC = (name) => {
  const value = `;${document.cookie}`;
  const parts = value.split(`;${name}=`);
  if (parts.length === 2) {
    return parts.pop().split(";").shift();
  }
};


const submitHandler = async (id) => {
  
  const text = document.getElementById(`textarea_${id}`).value;
  const content = document.getElementById(`content_${id}`);
  const modal = document.getElementById(`model_edit_post${id}`);

  try {
    const response = await fetch(`/editPost/${id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getC("csrftoken"),
      },
      body: JSON.stringify({ content: text }),
    });

    if (response.ok) {
      const result = await response.json();
      content.innerHTML = result.text;
      modal.classList.remove("show");
      modal.setAttribute("aria-hidden", "true");
      modal.setAttribute("style", "display:none");
      const modalsBackdrops = document.getElementsByClassName("modal-backdrop");
      for (let i = 0; i < modalsBackdrops.length; i++) {
        document.body.removeChild(modalsBackdrops[i]);
      }
    } else {
      throw new Error(
        `Error al actualizar la publicación. Estado: ${response.status}`
      );
    }
  } catch (error) {
    console.error(error);
  }
};

const menuBtn = document.querySelector('.menu-btn');
const menuContainer = document.querySelector('.menu-container');

menuBtn.addEventListener('click', () => {
  menuContainer.classList.toggle('active');
  menuContainer.setAttribute("style", "display:block");
});

