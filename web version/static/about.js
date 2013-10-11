function displayBar(e){
    var li=e.target.parentNode;
        console.log(li);
    for (var i=0;i<this.childNodes.length;++i) {
        this.childNodes[i].className="";
    }
    li.className="active";
}
document.getElementById("headBar").addEventListener("mouseover",displayBar);
