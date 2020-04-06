$(document).ready(function() {
    for (  var i = 16;  i < 31;  i++  ) {
      $('.sortable'+String(i)).sortable({
        cursor: 'move',
        opacity: 0.5,
        update: function(event, ui) {
          var serial = $('.sortable'+String(i)).sortable('serialize');
          $.ajax({
            url: "/book/sort",
            type: "post",
            data: serial
          });
        };
      });
    };
      for (  var i = 1;  i < 6;  i++  ) {
        $('.sortable'+String(i)).bind('sortstop',function(){
          // 番号を設定している要素に対しループ処理
            $(this).find('[name="num_data"]').each(function(idx){
          // タグ内に通し番号を設定（idxは0始まりなので+1する）
                $(this).html(idx+1);
            });
          });
      };
      for (  var i = 6;  i < 11;  i++  ) {
        $('.sortable'+String(i)).bind('sortstop',function(){
          // 番号を設定している要素に対しループ処理
            $(this).find('[name="num_data2"]').each(function(idx){
          // タグ内に通し番号を設定（idxは0始まりなので+1する）
                $(this).html(idx+1);
            });
          });
      };
      for (  var i = 11;  i < 16;  i++  ) {
        $('.sortable'+String(i)).bind('sortstop',function(){
          // 番号を設定している要素に対しループ処理
            $(this).find('[name="num_data3"]').each(function(idx){
          // タグ内に通し番号を設定（idxは0始まりなので+1する）
                $(this).html(idx+1);
            });
          });
      };
      for (  var i = 16;  i < 21;  i++  ) {
        $('.sortable'+String(i)).bind('sortstop',function(){
          // 番号を設定している要素に対しループ処理
            $(this).find('[name="num_data"]').each(function(idx){
          // タグ内に通し番号を設定（idxは0始まりなので+1する）
                $(this).html(idx+1);
            });
          });
      };
      for (  var i = 21;  i < 26;  i++  ) {
        $('.sortable'+String(i)).bind('sortstop',function(){
          // 番号を設定している要素に対しループ処理
            $(this).find('[name="num_data2"]').each(function(idx){
          // タグ内に通し番号を設定（idxは0始まりなので+1する）
                $(this).html(idx+1);
            });
          });
      };
      for (  var i = 26;  i < 31;  i++  ) {
        $('.sortable'+String(i)).bind('sortstop',function(){
          // 番号を設定している要素に対しループ処理
            $(this).find('[name="num_data3"]').each(function(idx){
          // タグ内に通し番号を設定（idxは0始まりなので+1する）
                $(this).html(idx+1);
            });
          });
      };
});
  for (  var i = 1;  i < 31;  i++  ) {
    $('.sortable'+String(i)).disableSelection();
  }

function done_alert() {
    alert('タスクを完了しました。\nおめでとうございます！！');
};