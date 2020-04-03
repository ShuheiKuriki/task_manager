$(document).ready(function() {
      $('.sortable1').sortable({
        cursor: 'move',
        opacity: 0.5,
        update: function(event, ui) {
          var serial = $('.sortable1').sortable('serialize');
          $.ajax({
            url: "/task/sort",
            type: "post",
            data: serial
          });
        }
      });
      $('.sortable2').sortable({
        cursor: 'move',
        opacity: 0.5,
        update: function(event, ui) {
          var serial = $('.sortable2').sortable('serialize');
          $.ajax({
            url: "/task/sort",
            type: "post",
            data: serial
          });
        }
      });
      $('.sortable3').sortable({
        cursor: 'move',
        opacity: 0.5,
        update: function(event, ui) {
          var serial = $('.sortable3').sortable('serialize');
          $.ajax({
            url: "/task/sort",
            type: "post",
            data: serial
          });
        }
      });
      $('.sortable4').sortable({
        cursor: 'move',
        opacity: 0.5,
        update: function(event, ui) {
          var serial = $('.sortable4').sortable('serialize');
          $.ajax({
            url: "/task/sort",
            type: "post",
            data: serial
          });
        }
      });
      $('.sortable5').sortable({
        cursor: 'move',
        opacity: 0.5,
        update: function(event, ui) {
          var serial = $('.sortable5').sortable('serialize');
          $.ajax({
            url: "/task/sort",
            type: "post",
            data: serial
          });
        }
      });
      $('.sortable6').sortable({
        cursor: 'move',
        opacity: 0.5,
        update: function(event, ui) {
          var serial = $('.sortable6').sortable('serialize');
          $.ajax({
            url: "/task/sort",
            type: "post",
            data: serial
          });
        }
      });
      $('.sortable7').sortable({
        cursor: 'move',
        opacity: 0.5,
        update: function(event, ui) {
          var serial = $('.sortable7').sortable('serialize');
          $.ajax({
            url: "/task/sort",
            type: "post",
            data: serial
          });
        }
      });
      $('.sortable8').sortable({
        cursor: 'move',
        opacity: 0.5,
        update: function(event, ui) {
          var serial = $('.sortable8').sortable('serialize');
          $.ajax({
            url: "/task/sort",
            type: "post",
            data: serial
          });
        }
      });
      $('.sortable9').sortable({
        cursor: 'move',
        opacity: 0.5,
        update: function(event, ui) {
          var serial = $('.sortable9').sortable('serialize');
          $.ajax({
            url: "/task/sort",
            type: "post",
            data: serial
          });
        }
      });
      $('.sortable10').sortable({
        cursor: 'move',
        opacity: 0.5,
        update: function(event, ui) {
          var serial = $('.sortable10').sortable('serialize');
          $.ajax({
            url: "/task/sort",
            type: "post",
            data: serial
          });
        }
      });
      $('.sortable11').sortable({
        cursor: 'move',
        opacity: 0.5,
        update: function(event, ui) {
          var serial = $('.sortable11').sortable('serialize');
          $.ajax({
            url: "/task/sort",
            type: "post",
            data: serial
          });
        }
      });
      $('.sortable12').sortable({
        cursor: 'move',
        opacity: 0.5,
        update: function(event, ui) {
          var serial = $('.sortable12').sortable('serialize');
          $.ajax({
            url: "/task/sort",
            type: "post",
            data: serial
          });
        }
      });
      $('.sortable13').sortable({
        cursor: 'move',
        opacity: 0.5,
        update: function(event, ui) {
          var serial = $('.sortable13').sortable('serialize');
          $.ajax({
            url: "/task/sort",
            type: "post",
            data: serial
          });
        }
      });
      $('.sortable14').sortable({
        cursor: 'move',
        opacity: 0.5,
        update: function(event, ui) {
          var serial = $('.sortable14').sortable('serialize');
          $.ajax({
            url: "/task/sort",
            type: "post",
            data: serial
          });
        }
      });
      $('.sortable15').sortable({
        cursor: 'move',
        opacity: 0.5,
        update: function(event, ui) {
          var serial = $('.sortable15').sortable('serialize');
          $.ajax({
            url: "/task/sort",
            type: "post",
            data: serial
          });
        }
      });
});

function done_alert() {
    alert('タスクを完了しました。\nおめでとうございます！！');
};