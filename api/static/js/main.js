// let socket = io();
// socket.on('connect', function () {
//     socket.emit('my event', {data: 'I\'m connected!'});
// });

// test ci
let to_update = document.getElementById('increment');

async function updateIncrement(){
    let val = await fetch('/update_increment');
    val = await val.text()
    to_update.innerHTML = val
}

// socket.on('updateIncrement', function(increment_int){
//     to_update.innerHTML = increment_int
// })

//

// setInterval(async ()=> {socket.emit('sock_update_increment')}, 10)