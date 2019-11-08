(function($) {
  var marker = {};

  marker.init = function(parent) {
    this.element = $(document.createElementNS('http://www.w3.org/2000/svg', 'circle'));
    this.radius = 5;
    this.element.attr({
      cx: $('input[name="latitude"]').val() | 0,
      cy: $('input[name="longitude"]').val() | 0,
      r: this.radius,
      fill: 'red'
    });
    this.element.appendTo(parent);
  }

  marker.set_position = function(x, y) {
    this.element.attr({
      cx: x,
      cy: y
    });
    // $('svg#Layer_1 path[cx="'+ x + '"][cy="' + y + ']"').
  }

  $(document).ready(function(){
    marker.init($('svg#Layer_1'));
  })

  $('svg#Layer_1').click(function(e){
    var svg = $(this)[0];
    var svgbox = svg.getAttribute('viewBox').split(/\s+|,/);

    var coords = {
      x: Math.round( e.offsetX * svgbox[2] / svg.clientWidth ),
      y: Math.round( e.offsetY * svgbox[3] / svg.clientHeight )
    }

    marker.set_position(coords.x, coords.y);
    $('input[name="latitude"]').val(coords.x);
    $('input[name="longitude"]').val(coords.y);
  });

})(django.jQuery);
