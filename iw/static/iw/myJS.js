function placeLayer(id) {
    let clicked = document.getElementById("facility"+id)
    clicked.setAttribute("onclick", "removeLayer(" + id + ")")
    clicked.setAttribute("class", "btn btn-primary")
    let parent = document.getElementsByClassName("plan_layers").item(0)
    parent.innerHTML += '<img src="/planImage/' + id + '" alt="nothing" id="facilityImage' + id + '"' + ' style="z-index:' + id + '">'
}

function removeLayer(id) {
    let clicked = document.getElementById("facility"+id)
    clicked.setAttribute("onclick", "placeLayer(" + id + ")")
    clicked.setAttribute("class", "btn btn-outline-primary")
    let parent = document.getElementsByClassName("plan_layers").item(0)
    parent.removeChild(document.getElementById("facilityImage" + id))
}


function updateError() {
}