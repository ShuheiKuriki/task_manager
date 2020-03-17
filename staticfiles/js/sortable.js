var classnames = ['.sortable1','.sortable2','.sortable3','.sortable4','.sortable5'];
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
  for (  var i = 1;  i < 6;  i++  ) {
      $('.sortable'+String(i)).disableSelection();
      $('.sortable'+String(i)).bind('sortstop',function(){
        // 番号を設定している要素に対しループ処理
          $(this).find('[name="num_data"]').each(function(idx){
        // タグ内に通し番号を設定（idxは0始まりなので+1する）
              $(this).html(idx+1);
          });
      });
  };
});

function done_alert() {
    alert('タスクを完了しました。\nおめでとうございます！！');
};