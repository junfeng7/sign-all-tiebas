function ajaxSubmit(e) {
    e.preventDefault();
    var megDiv=document.createElement("div");
    var form=this;
    for (var j=0;j<this.elements.length;++j) {
        field = this.elements[j];
        if (field.id=="oldpasswd"||field=="cookie") {
            if (!field.value) {
                megDiv.className="form-group has-warning";
                megDiv.innerHTML="<label class=\"control-label\">Please Input Value</label>";
                this.parentNode.insertBefore(megDiv,this);
                setTimeout(function() {
                        form.parentNode.removeChild(megDiv);
                }, 750);
                return;
            }
        }
    }
    var xhr=new XMLHttpRequest();
    xhr.open("POST",this.action,true);
    xhr.onreadystatechange=function() {
        if (xhr.readyState==4) {
            if (xhr.status==200) {
                response=JSON.parse(xhr.responseText);
                if (response.ok) {
                    
                    megDiv.className="form-group has-success";
                    megDiv.innerHTML="<label class=\"control-label\">"+response.ok+"</label>";
                }
                if (response.error) {
                    megDiv.className="form-group has-error";
                    megDiv.innerHTML="<label class=\"control-label\">"+response.error+"</label>";
                }
                form.parentNode.insertBefore(megDiv,form);
                setTimeout(function() {
                        form.parentNode.removeChild(megDiv);
                }, 750);
            }
            console.log(xhr.status+":"+xhr.statusText+"\n"+xhr.responseText);
        }
    }
    xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xhr.send(serialize(this));
}
function addListener() {
    for (var i=0;i<document.forms.length;++i) {
        document.forms[i].addEventListener("submit",ajaxSubmit);
    }
    document.getElementById("cookie").select()
}

function selectCookie()
{
    this.select();
}
document.addEventListener("DOMContentLoaded",addListener);
document.getElementById("cookie").addEventListener('focus',selectCookie);
