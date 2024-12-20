

function update(data) {
    cartQuantitys = document.getElementsByClassName('cart-counter');
    for (let cartQuan of cartQuantitys)
        cartQuan.innerText = data.total_quantity;

    cartAmounts = document.getElementsByClassName('cart-amount');
    for (let cartAmount of cartAmounts)
        cartAmount.innerText = data.total_amount;
}

function addToCart(id, name, price) {
    fetch(`/api/carts`, {
        method: "post",
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price
        }),
        headers: {
            "Content-type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        update(data);
    })
}

function updateCart(productId, obj) {
    fetch(`/api/carts/${productId}`, {
        method: "put",
        body: JSON.stringify({
            'quantity': obj.value
        }),
        headers: {
            "Content-type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        update(data)
    })
}

function deleteCart(productId) {
    if (confirm("do you want to delete this item?") === true){
        fetch(`/api/carts/${productId}`,{
            method: 'delete',
        }).then(res => res.json()).then(data => {
            update(data)
    
            document.getElementById(`cart_item${productId}`).style.display = "none";
        })
    }
}

function addComment(productId) {
    fetch(`/api/products/${productId}/comments`, {
        method: "post",
        body: JSON.stringify({
            'content': document.getElementById('comment').value
        }),
        headers: {
            "Content-type": "application/json"
        }
    }).then(res => res.json())
        .then(c => {
            let html = `
            <li class="list-group-item">

                <div class="row">
                    <div class="col-md-1 col-6">
                        <img src="${c.user.avatar}" class="rounded-circle" height="60" width="60" />
                    </div>
                    <div class="col-md-11 col-6">
                        <p>${c.content}</p>
                        <p class="date">${moment(c.created_date).locale("vi").fromNow()}</p>
                    </div>
                </div>

          </li>
        `;

            let h = document.getElementById("comments");
            h.innerHTML = html + h.innerHTML;
        })
}
