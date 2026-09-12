/* Availability calendar for OIA Suites Moalboal.
   Reads /data/availability.json: {updated, rooms:{slug:{name, booked:[YYYY-MM-DD,...]}}}
   A date in "booked" means the NIGHT of that date is not available. */
(function(){
  var DATA_URL='/data/availability.json';
  var data=null, view=new Date(), sel={room:null, start:null, end:null};
  var today=new Date(); today.setHours(0,0,0,0);
  var MONTHS=['January','February','March','April','May','June','July','August','September','October','November','December'];
  var DOW=['Mo','Tu','We','Th','Fr','Sa','Su'];
  var $=function(id){return document.getElementById(id);};
  function iso(d){return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');}
  function parse(s){var p=s.split('-');return new Date(+p[0],+p[1]-1,+p[2]);}
  function addDays(d,n){var x=new Date(d);x.setDate(x.getDate()+n);return x;}
  function isBooked(room,d){return data.rooms[room].booked.indexOf(iso(d))>=0;}
  function fmt(d){return d.toLocaleDateString('en-GB',{weekday:'short',day:'numeric',month:'short',year:'numeric'});}

  // ---- overview table
  function renderOverview(){
    var y=view.getFullYear(), m=view.getMonth(), days=new Date(y,m+1,0).getDate();
    $('cal-title').textContent=MONTHS[m]+' '+y;
    var h='<thead><tr><th>Suite</th>';
    for(var d=1;d<=days;d++){var dt=new Date(y,m,d),wk=dt.getDay()===0||dt.getDay()===6;h+='<th class="day'+(wk?' wk':'')+'" title="'+fmt(dt)+'">'+d+'</th>';}
    h+='</tr></thead><tbody>';
    Object.keys(data.rooms).sort().forEach(function(slug){
      var r=data.rooms[slug];
      h+='<tr><th class="room"><button type="button" data-room="'+slug+'">'+r.name+'</button></th>';
      for(var d=1;d<=days;d++){
        var dt=new Date(y,m,d),cls=[];
        if(dt<today)cls.push('past');else if(isBooked(slug,dt))cls.push('booked');
        if(iso(dt)===iso(today))cls.push('today');
        var label=r.name+' '+fmt(dt)+': '+(dt<today?'past':isBooked(slug,dt)?'booked':'available');
        h+='<td class="'+cls.join(' ')+'" title="'+label+'"><span class="sr-only">'+label+'</span></td>';
      }
      h+='</tr>';
    });
    h+='</tbody>';
    $('overview').innerHTML=h;
    $('overview').querySelectorAll('button[data-room]').forEach(function(b){b.addEventListener('click',function(){setRoom(b.getAttribute('data-room'));$('room-cal').scrollIntoView({behavior:'smooth',block:'start'});});});
  }

  // ---- month grid for one room
  function renderGrid(){
    var y=view.getFullYear(), m=view.getMonth(), days=new Date(y,m+1,0).getDate();
    var first=(new Date(y,m,1).getDay()+6)%7; // Monday first
    var h=DOW.map(function(d){return '<div class="dow">'+d+'</div>';}).join('');
    for(var i=0;i<first;i++)h+='<div class="empty"></div>';
    for(var d=1;d<=days;d++){
      var dt=new Date(y,m,d),cls=['day'],dis=false;
      var booked=isBooked(sel.room,dt);
      if(dt<today){cls.push('past');dis=true;}
      else if(booked){
        // a booked night can still be a check-out day if the previous night is free
        var prevFree=!isBooked(sel.room,addDays(dt,-1))&&addDays(dt,-1)>=today;
        if(sel.start&&!sel.end&&prevFree&&dt>sel.start){cls.push('checkout-ok');}else{cls.push('booked');dis=true;}
      }
      if(sel.start&&iso(dt)===iso(sel.start))cls.push('sel');
      if(sel.end&&iso(dt)===iso(sel.end))cls.push('sel');
      if(sel.start&&sel.end&&dt>sel.start&&dt<sel.end)cls.push('range');
      h+='<button type="button" class="'+cls.join(' ')+'" data-d="'+iso(dt)+'" '+(dis?'disabled aria-disabled="true"':'')+' aria-label="'+fmt(dt)+(booked?' booked':' available')+'">'+d+'</button>';
    }
    $('month-grid').innerHTML=h;
    $('month-grid').querySelectorAll('button.day:not([disabled])').forEach(function(b){b.addEventListener('click',function(){pick(parse(b.getAttribute('data-d')));});});
    renderSelection();
  }
  function rangeFree(a,b){for(var d=new Date(a);d<b;d=addDays(d,1)){if(isBooked(sel.room,d))return false;}return true;}
  function pick(d){
    if(!sel.start||sel.end||d<=sel.start){sel.start=d;sel.end=null;}
    else if(rangeFree(sel.start,d)){sel.end=d;}
    else{sel.start=d;sel.end=null;}
    renderGrid();
  }
  function renderSelection(){
    var t=$('selection-text'),f1=$('f-checkin'),f2=$('f-checkout');
    $('f-room').value=sel.room;$('room-select').value=sel.room;
    if(sel.start&&sel.end){
      var n=Math.round((sel.end-sel.start)/864e5);
      t.textContent=data.rooms[sel.room].name+': check-in '+fmt(sel.start)+', check-out '+fmt(sel.end)+' ('+n+' night'+(n>1?'s':'')+'). Fill in the form below to send the request.';
      f1.value=iso(sel.start);f2.value=iso(sel.end);
    }else if(sel.start){t.textContent='Arrival '+fmt(sel.start)+'. Now click the departure date.';f1.value=iso(sel.start);f2.value='';}
    else{t.textContent='Select an arrival date and a departure date in the calendar.';}
  }
  function setRoom(slug){if(!data.rooms[slug])return;sel={room:slug,start:null,end:null};renderGrid();}

  function init(){
    var q=new URLSearchParams(location.search).get('room');
    sel.room=(q&&data.rooms[q])?q:Object.keys(data.rooms)[0];
    var upd=data.updated?new Date(data.updated):null;
    $('avail-updated').textContent='Availability last updated '+(upd?upd.toLocaleString('en-GB',{day:'numeric',month:'long',year:'numeric',hour:'2-digit',minute:'2-digit'}):'today')+' from the booking platform calendars. Bookings made on the platforms in the meantime are picked up at the next daily update, which is why every request is checked by the team before confirmation.';
    renderOverview();renderGrid();
    $('prev-month').addEventListener('click',function(){view=new Date(view.getFullYear(),view.getMonth()-1,1);renderOverview();renderGrid();});
    $('next-month').addEventListener('click',function(){view=new Date(view.getFullYear(),view.getMonth()+1,1);renderOverview();renderGrid();});
    $('room-select').addEventListener('change',function(){setRoom(this.value);});
    $('f-room').addEventListener('change',function(){setRoom(this.value);});
    $('f-checkin').addEventListener('change',function(){var d=parse(this.value);if(!isNaN(d)){sel.start=d;sel.end=null;view=new Date(d.getFullYear(),d.getMonth(),1);renderOverview();renderGrid();}});
    $('f-checkout').addEventListener('change',function(){var d=parse(this.value);if(!isNaN(d)&&sel.start&&d>sel.start){sel.end=d;renderGrid();}});
    $('next-url').value=location.origin+'/request-sent/';
    $('request-form').addEventListener('submit',function(e){
      var err=$('form-error');err.hidden=true;
      var a=$('f-checkin').value,b=$('f-checkout').value,room=$('f-room').value;
      var msg='';
      if(!a||!b)msg='Please choose a check-in and a check-out date.';
      else if(parse(b)<=parse(a))msg='Check-out must be after check-in.';
      else if(!rangeFree(parse(a),parse(b))&&data.rooms[room])msg=data.rooms[room].name+' is not available on all of those nights. Pick other dates or another suite, or send the request anyway with a note and the team will suggest alternatives.';
      var req=this.querySelectorAll('[required]');for(var i=0;i<req.length;i++){if(!req[i].value){msg=msg||'Please fill in name, e-mail and dates.';}}
      if(msg&&!(msg.indexOf('not available')>=0&&this.getAttribute('data-force')==='1')){e.preventDefault();err.textContent=msg;err.hidden=false;if(msg.indexOf('not available')>=0){this.setAttribute('data-force','1');err.textContent+=' Click "Send booking request" again to send it anyway.';}}
    });
  }
  fetch(DATA_URL,{cache:'no-store'}).then(function(r){return r.json();}).then(function(j){data=j;init();}).catch(function(){
    $('avail-updated').textContent='The live calendar could not be loaded. Send the request with preferred dates and the team will confirm availability.';
    $('overview').hidden=true;$('room-cal').hidden=true;
  });
})();
