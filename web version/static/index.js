function addTiebas(e) {
    var megDiv=document.createElement("div");

    var table=document.getElementById("contents");
    var button=document.getElementById("addTiebas");
    var input=document.getElementById("tiebas");
    if (!input.value) {
        megDiv.className="form-group has-warning";
        megDiv.innerHTML="<label class=\"control-label\" style=\"padding-left:20px;\">Please Input Value</label>";
        button.parentNode.parentNode.insertBefore(megDiv,button.parentNode);
        setTimeout(function() {
            button.parentNode.parentNode.removeChild(megDiv);
        }, 750);
        return;
    }
    var separate=" "
    if (input.value.search("　")!=-1) {
        separate="　";
    }
    var tiebas=input.value.split(separate);
    for (var i=0;i<tiebas.length;++i) {
        tiebas[i]=encodeURIComponent(tiebas[i]);
    }
    var xhr=new XMLHttpRequest();
    xhr.open("POST","/?action=add",true);
    xhr.onreadystatechange=function() {
        if (xhr.readyState==4) {
            if (xhr.status==200) {
                var response=JSON.parse(xhr.responseText);
                if (response.rep=="ok") {
                    
                    megDiv.className="form-group has-success";
                    megDiv.innerHTML="<label class=\"control-label\">Successfully add</label>";
                }
                if (response.rep=="error") {
                    megDiv.className="form-group has-error";
                    megDiv.innerHTML="<label class=\"control-label\">"+response.data+"</label>";
                }
                table.parentNode.insertBefore(megDiv,table);
                setTimeout(function() {
                    table.parentNode.removeChild(megDiv);
                }, 750);
            }
            console.log(xhr.status+":"+xhr.statusText+"\n"+xhr.responseText);
            if (response.rep=="ok") {
                for (var j=0;j<response.data.c;++j) {
                    var row=table.insertRow(-1);
                    row.innerHTML="<td><input type=\"checkbox\" name=\"tieba\" value=\""+response.data[j]+"\"></td><td>"+response.data[j]+"</td><td>First add,unknown signed time</td><td>No sign info</td><td>Not sign today</td><td><a href=\"#delete\" title=\"delete "+response.data[j]+"吧\" style=\"color:black;\"><i class=\"glyphicon glyphicon-remove\"></i></a></td>";
                    row.lastElementChild.lastElementChild.addEventListener("click",deleteTieba);
                }
            }
        }
    };

    xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xhr.send("tiebas="+JSON.stringify(tiebas));
    console.log("after send");
    $("#myModal").modal("hide");
    input.value="";

}
function selectAll() {
   var tiebas=document.getElementsByName("tieba");
   console.log(tiebas);
   if (!allSelect) {
       this.innerText="Invert Select";
   }
   else {
       this.innerText="Select All";
   }
   for (var i=0;i<tiebas.length;++i) {
        tiebas[i].checked=!tiebas[i].checked;
   }
   allSelect=!allSelect;
}



function deleteTieba() {
    var megDiv=document.createElement("div");

    var table=document.getElementById("contents");
    var tiebasToDelete=[];
    var nodesToDelete=[];
    if (this.id=="deleteSelected") {
        var tiebasCheckbox=document.getElementsByName("tieba");
        for (var i=0;i<tiebasCheckbox.length;++i) {
            if (tiebasCheckbox[i].checked) {
                tiebasToDelete.push(encodeURIComponent(tiebasCheckbox[i].value));
                //nodesToDelete.push(tiebasCheckbox[i].parentNode.parentNode);
            }
        }
    }
    else{
        if(this.id="deleteOne") {
            tiebasToDelete.push(encodeURIComponent(this.title.slice(7,this.title.length-1)));
            //nodesToDelete.push(this.parentNode.parentNode);
        }
    }
    if (tiebasToDelete.length==0) {
        megDiv.className="form-group has-warning";
        megDiv.innerHTML="<label class=\"control-label\" style=\"padding-left:20px;\">Please select one at least first.</label>";
        table.parentNode.insertBefore(megDiv,table);
        setTimeout(function() {
            table.parentNode.removeChild(megDiv);
        }, 750);
        return ;
    }
    var xhr=new XMLHttpRequest();
    xhr.open("POST","/?action=delete",true);
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

                //according to response.data delete tieba node 
                var tiebasCheckbox=document.getElementsByName("tieba");
                for (var i=0;i<response.data['c'];++i) {
                    for (var j=0;j<tiebasCheckbox.length;++j) {
                        console.log(tiebasCheckbox[j])
                        if (tiebasCheckbox[j].value==response.data[i]) {
                            nodesToDelete.push(tiebasCheckbox[j].parentNode.parentNode);
                            break;
                        }
                    }
                }
                for (var j=0;j<nodesToDelete.length;++j) {
                    console.log(nodesToDelete[j]);
                    table.tBodies[0].removeChild(nodesToDelete[j]);
                }
            }
            console.log(xhr.status+":"+xhr.statusText+"\n"+xhr.responseText);
        }
    };

    xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xhr.send("tiebas="+JSON.stringify(tiebasToDelete));
}


function signAll() {
    var megDiv=document.createElement("div");

    var table=document.getElementById("contents");
    var tiebasToSign=[];
    var nodesToUpdate=[];
    var tiebasCheckbox=document.getElementsByName("tieba");
    var check=false;
    for (var i=0;i<tiebasCheckbox.length;++i) {
        if (tiebasCheckbox[i].checked) {
            check=true;
            var time=tiebasCheckbox[i].parentNode.nextElementSibling.nextElementSibling.lastElementChild;
            console.log(time);
            if (time){
                if(time.value=="0") {
                    continue;
                }
                console.log(time.value);
                var signtime=new Date(Number(time.value+"000")).toLocaleDateString();
                var now=new Date().toLocaleDateString();
                console.log(signtime+"="+now);
                if (now==signtime) {
                    continue;
                }
            }
            tiebasToSign.push(encodeURIComponent(tiebasCheckbox[i].value));
        }
    }
    console.log(tiebasToSign);
    if (tiebasToSign.length==0) {
        megDiv.className="form-group has-warning";
        if (!check) {
            megDiv.innerHTML="<label class=\"control-label\" style=\"padding-left:20px;\">Please Select at least one.</label>";
        }
        else {
            megDiv.innerHTML="<label class=\"control-label\" style=\"padding-left:20px;\">these tiebas you selected have been signed today.</label>";

        }
        table.parentNode.insertBefore(megDiv,table);
        setTimeout(function() {
            table.parentNode.removeChild(megDiv);
        }, 750);
        return ;
    }
    var xhr=new XMLHttpRequest();
    xhr.open("POST","/?action=sign",true);
    xhr.onreadystatechange=function() {
        if (xhr.readyState==4) {
            if (xhr.status==200) {
                var response=JSON.parse(xhr.responseText);
                if (response.rep=="ok") {
                    
                    megDiv.className="form-group has-success";
                    megDiv.innerHTML="<label class=\"control-label\">Successfully Sign</label>";
                }
                if (response.rep=="error") {
                    megDiv.className="form-group has-error";
                    megDiv.innerHTML="<label class=\"control-label\">"+response.data+"</label>";
                }
                table.parentNode.insertBefore(megDiv,table);
                setTimeout(function() {
                    table.parentNode.removeChild(megDiv);
                }, 750);

                //according to response.data update tieba node 
                var tiebasCheckbox=document.getElementsByName("tieba");
                for (var i=0;i<response.data['c'];++i) {
                    var meg=response.data[i]['meg'];
                    for (var j=0;j<tiebasCheckbox.length;++j) {
                         console.log(tiebasCheckbox[j].value==response.data[i]['tieba']);
                        if (tiebasCheckbox[j].value==response.data[i]['tieba']) {
                            var tr=tiebasCheckbox[j].parentNode.parentNode;
                            var tds=tr.childNodes;
                            // success condition fucking do.
                            if (meg['no']==0&&!meg['error']) {
                                var uinfo=meg['data']['uinfo'];
                                console.log(uinfo);
                                var now=new Date(Number(meg["data"]["uinfo"]["sign_time"]+"000"));
                                tds[2].innerHTML=now.toLocaleString()+"<input type=\"hidden\" name=\"sign_time\" value=\""+meg["data"]["uinfo"]["sign_time"]+"\">";
                                tds[3].innerText="cont_sign_num:"+uinfo["cont_sign_num"]+" cout_total_sing_num:"+uinfo["cout_total_sing_num"]+" user_sign_rank:"+uinfo["user_sign_rank"];
                                tds[4].innerHTML="<div class=\"form-group has-success\"><label class=\"control-label\">successfully signed</label></div>"
                            }
                            // error condition fucking do.
                            else {
                                if (meg['no']!=4) {
                                    tds[2].innerHTML=new Date().toLocaleString+"<input type=\"hidden\" name=\"sign_name\" value=\"0\">";
                                }
                                else {
                                    tds[2].innerText="Unknown last sign time";
                                }
                                tds[3].innerText=meg['error'];
                                var error;
                                if (meg['no']==1101){
                                    error="repeat sign today";
                                }
                                else if(meg['no']==1010) {
                                    error="No this name tieba"
                                }
                                else if(meg['no']==4){
                                    error="<a href=\"/settings\" title=\"please modify your cookie.\">Cookie Invalid</a>";
                                }
                                else {
                                    error="Unknown error.";
                                }
                                tds[4].innerHTML="<div class=\"form-group has-error\"><label class=\"control-label\">"+error+"</lable></div>";
                            }

                            break;
                        }
                    }
                }
            }
            console.log(xhr.status+":"+xhr.statusText+"\n"+xhr.responseText);
        }
    };
    xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xhr.send("tiebas="+JSON.stringify(tiebasToSign));
    check=false;

}
function enterAction(e) {
    if (e.keyCode==13) {
        addTiebas();
    }
}

allSelect=false;
document.getElementById("addTiebas").addEventListener("click",addTiebas);
document.getElementById("selectAll").addEventListener("click",selectAll);
document.getElementById("deleteSelected").addEventListener("click",deleteTieba);
document.getElementById("signAll").addEventListener("click",signAll);
document.getElementById("tiebas").addEventListener("keypress",enterAction);


var tiebasDeleteFromA=document.getElementsByName("tiebaToDelete");
for (var k=0;k<tiebasDeleteFromA.length;++k) {
    tiebasDeleteFromA[k].addEventListener("click",deleteTieba);
}
