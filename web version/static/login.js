function Submit(e) {
    e.preventDefault();
    var divParent=this.parentNode;
    var formId=divParent.id;
    var errorInput=false;
    var form=this;
    var emailMatch=/^([a-zA-Z0-9]+[.|-|_]*)*[a-zA-Z0-9]+_*@([a-zA-Z0-9]+[.|-]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
    for (var i=0;i<this.elements.length;++i) {
        var field=this.elements[i];
        if (field.tagName=="INPUT") {
            var input=field;
            if (!input.value) {
                errorInput=true;
                megDiv.className="form-group has-warning";
                megDiv.innerHTML="<label class=\"control-label\" style=\"padding-left:20px;\">Please Input Value</label>";
                break;
            }
            if (input.name=="email"){
                if (!emailMatch.test(input.value)) {
                    errorInput=true;
                    megDiv.className="form-group has-error";
                    megDiv.innerHTML="<label class=\"control-label\" style=\"padding-left:20px;\">Email Address Invalid</label>";
                    break;
                }
            }
        }
    }
    if (errorInput){
        divParent.insertBefore(megDiv,this);
        setTimeout(function() {
            divParent.removeChild(megDiv);
        }, 750);
        return;
    }
    var xhr=new XMLHttpRequest();
    var url=formId=="login"?document.URL:"/sign";
    xhr.open("POST",url,true);
    xhr.onreadystatechange=function() {
        if (xhr.readyState==4) {
            if (xhr.status==200) {
                var response=JSON.parse(xhr.responseText);
                if (response.rep=="ok") {
                    
                    megDiv.className="form-group has-success";
                    megDiv.innerHTML="<label class=\"control-label\">"+response.data+"</label>";
                }
                if (response.rep=="error") {
                    megDiv.className="form-group has-error";
                    megDiv.innerHTML="<label class=\"control-label\">"+response.data+"</label>";
                }
                divParent.insertBefore(megDiv,form);
                setTimeout(function() {
                    divParent.removeChild(megDiv);
                if (response.rep=="ok") {
                    if (formId=="login") {
                        window.location=response.url;
                    }
                    else {
                        if (formId=="create") {
                            form.reset();
                            $("#myTab a:first").tab("show");
                        }
                    }
                }
                }, 750);

            }
            console.log(xhr.status+":"+xhr.statusText+"\n"+xhr.responseText);
        }
    };

    xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xhr.send(serialize(form));
    
}

var megDiv=document.createElement("div");
for (var i=0;i<document.forms.length;++i){
    document.forms[i].addEventListener("submit",Submit);
}
