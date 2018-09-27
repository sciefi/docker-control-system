$(document).ready(function () {

    var create_click_handler = function(action, key) {
      return function() {command(action, key)};
    }

  //common function for all the route actions
    function command(action, id) {
        RPC.call(action, id).then(
            function (message) {
                alert(message);
                get_containers();
            });
    }

    function get_images() {
        RPC.call('route.get_images').then(function (images) {
            $('#images-list').empty();
            for (var id in images) {
                $('#images-list').append("<a class='list-group-item' data-toggle='list' role='tab' id=" + id + "_" + ">" + images[id] + "<button type='button' style='float: right;' id=" + id + ">Run</button>" + "</a>");
                document.getElementById(id).onclick = create_click_handler('route.run', id);
            }
        }).done();
    }

    function get_containers() {
          RPC.call('route.get_containers', [false]).then(function (active_containers) {
                $('#containers-list').empty();
                for (var id in active_containers) {
                $('#containers-list').append("<a class='list-group-item list-group-item-success' id=" + id + ">" + active_containers[id] + "<button type='button' style='float: right;' id=stop" + id + ">Stop</button>" + "</a>");
                document.getElementById("stop"+id).onclick = create_click_handler('route.stop', id);
              }
            }).done();

            RPC.call('route.get_containers', [true]).then(function (containers) {
                for (var id in containers) {
                  if (document.getElementById(id) == null){
                  $('#containers-list').append("<a class='list-group-item list-group-item-danger' id=" + id + ">" + containers[id] + "<button type='button' style='float: right;' id=restart" + id + ">Restart</button>"  +"<button type='button' style='float: right;' id=remove" + id + ">Remove</button>"  + "</a>");
                  document.getElementById("remove"+id).onclick = create_click_handler('route.remove', id);
                  document.getElementById("restart"+id).onclick = create_click_handler('route.restart', id);
                }
              }
            }).done();
    }

    var url = (window.location.protocol === "https:" ? "wss://" : "ws://") + window.location.host + '/ws/';
    RPC = WSRPC(url, 5000);
    RPC.connect();
    get_images();
    get_containers();
});
