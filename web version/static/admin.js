function selectAll() {
   var users=document.getElementsByName("user");
   console.log(users);
   if (!allSelect) {
       this.innerText="Invert Select";
   }
   else {
       this.innerText="Select All";
   }
   for (var i=0;i<users.length;++i) {
        users[i].checked=!users[i].checked;
   }
   allSelect=!allSelect;
}

function deleteUsers() {
    var megDiv=document.createElement("div");
    var usersToDelete=[];
    var nodesToDelete=[];
    
    this.disabled=true;
    if (this.id=="deleteSelected") {
        var usersCheckbox=document.getElementsByName("user");
        for (var i=0;i<usersCheckbox.length;++i) {
            if (usersCheckbox[i].checked) {
                usersToDelete.push(encodeURIComponent(usersCheckbox[i].value));
            }
        }
    }
    else{
        if(this.id="deleteOne") {
            usersToDelete.push(encodeURIComponent(this.name));
        }
    }
    if (usersToDelete.length==0) {
        megDiv.className="form-group has-warning";
        megDiv.innerHTML="<label class=\"control-label\" style=\"padding-left:20px;\">Please select at least one user first.</label>";
        table.parentNode.insertBefore(megDiv,table);
        setTimeout(function() {
            table.parentNode.removeChild(megDiv);
        }, 750);
        this.disabled=false;
        return ;
    }
    var xhr=new XMLHttpRequest();
    xhr.open("POST","/admin",true);
    xhr.onreadystatechange=function() {
        if (xhr.readyState==4) {
            if (xhr.status==200) {
                var response=JSON.parse(xhr.responseText);
                if (response.rep=="ok") {
                    
                    megDiv.className="form-group has-success";
                    megDiv.innerHTML="<label class=\"control-label\">Successfully delete</label>";
                }
                if (response.rep=="error") {
                    megDiv.className="form-group has-error";
                    megDiv.innerHTML="<label class=\"control-label\">"+response.data+"</label>";
                }
                table.parentNode.insertBefore(megDiv,table);
                setTimeout(function() {
                    table.parentNode.removeChild(megDiv);
                }, 750);

                if (response.rep=='ok'){
                //according to response.data delete tieba node 
                    var usersCheckbox=document.getElementsByName("user");
                    for (var i=0;i<response.data['c'];++i) {
                        for (var j=0;i<usersCheckbox.length;++j) {
                            if (usersCheckbox[j].value==response.data[i]) {
                                nodesToDelete.push(usersCheckbox[j].parentNode.parentNode);
                                break;
                            }
                        }
                    }
                    for (var j=0;j<nodesToDelete.length;++j) {
                        console.log(nodesToDelete[j]);
                        table.tBodies[0].removeChild(nodesToDelete[j]);
                    }
                }
            }
            this.disabled=false;
            console.log(xhr.status+":"+xhr.statusText+"\n"+xhr.responseText);
        }
    };

    xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xhr.send("users="+JSON.stringify(usersToDelete));
}

allSelect=false;
var table=document.getElementById("usersTable");
document.getElementById("selectAll").addEventListener("click",selectAll);
document.getElementById("deleteSelected").addEventListener("click",deleteUsers);
var usersDeleteFromA=document.getElementsByClassName("userA");
for (var k=0;k<usersDeleteFromA.length;++k) {
    usersDeleteFromA[k].addEventListener("click",deleteUsers);
}
