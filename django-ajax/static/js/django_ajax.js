console.log('django_ajax.js is start')
var cookies = parse_cookies();
console.log(cookies);
var result = document.getElementById('result');


function submit_in_post() {
    var xhr = new XMLHttpRequest();
    var data = {'user':'index'};
    var json = JSON.stringify(data);
    console.log(json);
    xhr.open('POST', 'ajax_post/');
    xhr.setRequestHeader('X-CSRFToken', cookies['csrftoken']);
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4){
            if (xhr.status === 200){
                console.log(post_result);
            }else{
                console.log(xhr.status);
                console.log('submit_in_get is failed...');
            }
        }else{
            console.log('通信中...');
        };
    };
    xhr.send(json);
};

document.getElementById('submit_in_get').addEventListener('click', function(){
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'ajax_get/');
    xhr.onload = function () {
        if (xhr.readyState === 4){
            if (xhr.status === 200){
                console.log(xhr.responseText);
            }else{
                console.log(xhr.status);
                console.log('submit_in_get is failed...');
            }
        };
    }
    xhr.send(null);
    result.textContent = "get!";
}, false);

document.getElementById('submit_in_post').addEventListener('click',function () {
    result_txt = submit_in_post();
    result.textContent = "clicked...";
});

console.log(result);
