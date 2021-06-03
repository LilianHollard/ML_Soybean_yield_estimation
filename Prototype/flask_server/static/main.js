var app = new Vue({
    el: '#select_city',
    delimiters: ['((', '))'],
    data: {
      SM_show:false,
      CN_show:false
    },
    methods: {
      changeToSantaMaria: function(){
        this.SM_show = true
        this.CN_show = false
      },
      changeToCamposNovos: function(){
        this.SM_show = false
        this.CN_show = true
      }
    }
  })



$(document).on('submit','#SantaMariaForm',function(e){
  console.log('start');
  e.preventDefault();
  $.ajax({
    type:'POST',
    url:'/',
    data: $("#SantaMariaForm").serialize(),
    success: function() {
      console.log("Send data");
      document.getElementById("SantaMariaForm").reset();
    }
  });
});

$(document).on('submit','#CamposNovosForm',function(e){
  console.log('start');
  e.preventDefault();
  $.ajax({
    type:'POST',
    url:'/',
    data: $("#CamposNovosForm").serialize(),
    success: function() {
      console.log("Send data");
      document.getElementById("CamposNovosForm").reset();
    }
  });
});