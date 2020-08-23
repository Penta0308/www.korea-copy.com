//
// Little Net Javascript Common Functions (Utility)
// lutil.js
// 2003-03-29 : new create  (A.MORI)
// 2011-01-20 : last update (A.MORI)
// [UTF-8]
//

// modal form open
function ltu_modalbox_open(
	p_id_window,				// (I) open window element id
	p_id_overlay,				// (I) overlay element id
	p_vpos_from_top,			// (I) vertical position from top / expl) 50
	p_hpos_from_center)			// (I) horizontal position from top / expl) -50
{
	var p_scr_y = document.documentElement.scrollTop || document.body.scrollTop || 0;
	var p_vpos  = p_vpos_from_top + p_scr_y;
	var p_ele_window  = document.getElementById(p_id_window);
	var p_ele_overlay = document.getElementById(p_id_overlay);

	var doc_width  = document.documentElement.scrollWidth || document.body.scrollWidth;
	var doc_height = document.documentElement.scrollHeight || document.body.scrollHeight;

	p_ele_overlay.style.width	= doc_width + 'px';
	p_ele_overlay.style.height	= doc_height + 'px';
	p_ele_overlay.style.display	= 'block';

	p_ele_window.style.margin	= p_vpos + 'px 0px 0px ' + p_hpos_from_center + 'px';
	p_ele_window.style.display	= 'block';
}

// modal form close
function ltu_modalbox_close(
	p_id_window,				// (I) open window element id
	p_id_overlay)				// (I) overlay element id
{
	var p_ele_window  = document.getElementById(p_id_window);
	var p_ele_overlay = document.getElementById(p_id_overlay);

	p_ele_overlay.style.display	= 'none';
	p_ele_window.style.display	= 'none';
}

// get element width
function ltu_element_width(	// (R) element width
	p_ele)	// (I) element
{
	var result = 0;
	if      (p_ele.offsetWidth)						{ result = p_ele.offsetWidth; }
	else if (p_ele.clip && p_ele.clip.width)		{ result = p_ele.clip.width; }
	else if (p_ele.style && p_ele.style.pixelWidth)	{ result = p_ele.style.pixelWidth; }
	return parseInt(result);
}

// get element height
function ltu_element_height(	// (R) element height
	p_ele)	// (I) element
{
	var result = 0;
	if      (p_ele.offsetHeight)					{ result = p_ele.offsetHeight; }
	else if (p_ele.clip && p_ele.clip.height)		{ result = p_ele.clip.height; }
	else if (p_ele.style && p_ele.style.pixelHeight){ result = p_ele.style.pixelHeight; }
	return parseInt(result);
}

// string trim
function ltu_str_trim(p_str)
{
	return p_str.replace(/(^\s+)|(\s+$)/g, "");
}

// get object field value
function ltu_get_obj_fld_value(fld)
{
  if (fld.type.substr(0,6) == 'select')
  {
    n_sel = fld.selectedIndex;
    if (n_sel < 0) { return ''; }
    return fld.options[n_sel].value;
  }

  return fld.value;
}

// get object field value (type2)
function ltu_get_obj_fld_value2(fm_obj, el_name)
{
  var i;

  nele = fm_obj.elements.length;
  for(i = 0; i < nele; i ++)
  {
    if (fm_obj.elements[i].name == el_name)
    {
      el_obj = fm_obj.elements[i];
      if (el_obj.type.substr(0,6) == 'select')
      {
        n_sel = el_obj.selectedIndex;
        if (n_sel < 0) { return ''; }
        return el_obj.options[n_sel].value;
      }
      else if (el_obj.type.substr(0,5) == 'radio')
      {
        if (el_obj.checked) { return el_obj.value; }
      }
      else
      {
        return el_obj.value;
      }
    }
  }
  return '';
}

// set object field value
function ltu_set_obj_fld_value(fld, val)
{
  var i;

  if (fld.type.substr(0,6) == 'select')
  {
    for (i = 0; i < fld.length; i ++)
    {
      if (fld.options[i].value == val)
      {
        fld.selectedIndex = i;
        return;
      }
    }
  }
  else
  {
    fld.value = val;
  }
}

// set object field value(type2)
function ltu_set_obj_fld_value2(fm_obj, el_name, val)
{
  var i;
  var j;

  nele = fm_obj.elements.length;
  for(i = 0; i < nele; i ++)
  {
    if (fm_obj.elements[i].name == el_name)
    {
      el_obj = fm_obj.elements[i];
      if (el_obj.type.substr(0,6) == 'select')
      {
        for (j = 0; j < el_obj.length; j ++)
        {
          if (el_obj.options[j].value == val)
          {
            el_obj.selectedIndex = j;
            return;
          }
        }
      }
      else if (el_obj.type.substr(0,5) == 'radio')
      {
        if (el_obj.value == val)
        {
          el_obj.checked = true;
          return;
        }
      }
      else
      {
        el_obj.value = val;
      }
    }
  }
}

// field exist check
function ltu_chk_fld_exist(fld, name)
{
  fld_value = ltu_get_obj_fld_value(fld);
  if (fld_value == '')
  {
    alert(name + 'を指定して下さい。');
	fld.focus();
    return false;
  }
  return true;
}

// field checked check (for radio)
function ltu_chk_fld_check(fld, name)
{
  var i;

  if (fld.length == void(0))
  {
    if (fld.checked) { return true; }
    alert(name + 'を指定して下さい。');
    fld.focus();
  }
  else
  {
    for (i = 0; i < fld.length; i++)
    {
      if (fld[i].checked) { return true; }
    }
    alert(name + 'を指定して下さい。');
    fld[0].focus();
  }
  return false;
}

// field checked check (for checkbox)
function ltu_chk_fld_chkbox(fld, name)
{
  if (fld.checked) { return true; }
  alert(name + 'を指定して下さい。');
  fld.focus();
  return false;
}

// field checked check (for multi checkbox)
function ltu_chk_fld_chkboxes(obj_form, elname, name)
{
  var i;

  obj_fld = obj_form.elements[0];
  chk_cnt = 0;
  for (i = obj_form.elements.length - 1; i >= 0; i --)
  {
    if (obj_form.elements[i].name == elname)
    {
      obj_fld = obj_form.elements[i];
      if (obj_fld.checked) { chk_cnt ++; }
    }
  }
  if (chk_cnt > 0) { return true; }
  alert(name + 'を指定して下さい。');
  obj_fld.focus();
  return false;
}

// field length check
function ltu_chk_fld_len(fld, len1, len2, name)
{
  if (fld.value.length < len1 || fld.value.length > len2)
  {
    if (len1 == 0)
    {
      alert(name + 'は ' + len2 + ' 文字以内を指定して下さい。');
    }
    else if (len1 == len2)
    {
      alert(name + 'は ' + len1 + ' 文字を指定して下さい。');
    }
    else
    {
      alert(name + 'は ' + len1 + '～' + len2 + ' 文字を指定して下さい。');
    }
    fld.focus();
    return false;
  }
  return true;
}

// field mail check
function ltu_chk_fld_mail(fld, name)
{
  if (fld.value != '')
  {
    if (!fld.value.match(/.+@.+\..+/i))
    {
      alert(name + 'に半角英数字で正しいアドレスが入力されているか確認して下さい。');
	  fld.focus();
      return false;
    }
  }
  return true;
}
function ltu_chk_fld_mail2(fld, name)
{
  if (!ltu_chk_fld_exist(fld, name)) { return false; }
  return ltu_chk_fld_mail(fld, name);
}

// field tel check
function ltu_chk_fld_tel(fld, name)
{
  if (fld.value != '')
  {
    if (!fld.value.match(/^[0-9]+\-[0-9]+\-[0-9]+$/i))
    {
      alert(name + 'に半角数字とハイフンで正しい番号が入力されているか確認して下さい。');
	  fld.focus();
      return false;
    }
  }
  return true;
}
function ltu_chk_fld_tel2(fld, name)
{
  if (!ltu_chk_fld_exist(fld, name)) { return false; }
  return ltu_chk_fld_tel(fld, name);
}

// field number check
function ltu_chk_fld_num(fld, min, max, name)
{
  if (fld.value != '')
  {
    if (!fld.value.match(/^[0-9]+$/i))
    {
      alert(name + 'には数値を指定して下さい。');
	  fld.focus();
      return false;
    }
    if (min < max)
    {
      if (fld.value < min || max < fld.value)
      {
        alert(name + 'には ' + min + '～' + max +' の数値を指定して下さい。');
	    fld.focus();
        return false;
      }
    }
  }
  return true;
}
function ltu_chk_fld_num2(fld, min, max, name)
{
  if (!ltu_chk_fld_exist(fld, name)) { return false; }
  return ltu_chk_fld_num(fld, min, max, name);
}

// field number - check
function ltu_chk_fld_numh(fld, name)
{
  if (fld.value != '')
  {
    if (!fld.value.match(/^[0-9-]+$/i))
    {
      alert(name + 'には数値とハイフンを指定して下さい。');
	  fld.focus();
      return false;
    }
  }
  return true;
}
function ltu_chk_fld_numh2(fld, name)
{
  if (!ltu_chk_fld_exist(fld, name)) { return false; }
  return ltu_chk_fld_numh(fld, name);
}

// field number abc check
function ltu_chk_fld_numa(fld, name)
{
  if (fld.value != '')
  {
    if (!fld.value.match(/^[0-9a-zA-Z-_]+$/i))
    {
      alert(name + 'には半角英数を指定して下さい。');
	  fld.focus();
      return false;
    }
  }
  return true;
}
function ltu_chk_fld_numa2(fld, name)
{
  if (!ltu_chk_fld_exist(fld, name)) { return false; }
  return ltu_chk_fld_numa(fld, name);
}

// set cookie
function ltu_set_cookie(cnam, cval)
{
  dt_exp = new Date();
  dt_exp.setTime(dt_exp.getTime() + 1000*60*60*24*365);
  document.cookie = cnam + "=" + escape(cval) + "; expires=" + dt_exp.toGMTString();
}

// get cookie
function ltu_get_cookie(cnam, cdef)
{
  var i;

  cookies = document.cookie.split("; ");
  for (i = 0; i < cookies.length; i++)
  {
    vals = cookies[i].split("=");
    if (cnam == vals[0] && vals.length > 1)
    {
      return unescape(vals[1]);
    }
  }
  return cdef;
}

// set default cookie to fields
function ltu_setdef_cookie_to_fld(fm_obj, cookie_name)
{
  var i, j;

  // get cookie for fields default
  wstr  = ltu_get_cookie(cookie_name, "");
  wstrs = wstr.split("\t");
  for(i = 0; i < wstrs.length - 1; )
  {
    cook_name  = wstrs[i]; i ++;
    cook_value = wstrs[i]; i ++;
    if (cook_name.indexOf("[]") >= 0)
    {
      obj_checked = false;
      for(j = 0; j < fm_obj.elements.length; j ++)
      {
        el_obj = fm_obj.elements[j];
        if (el_obj.name == cook_name && el_obj.checked) { obj_checked = true; break; }
      }
      if (!obj_checked)
      {
        for(j = 0; j < fm_obj.elements.length; j ++)
        {
          el_obj = fm_obj.elements[j];
          if (el_obj.name == cook_name && cook_value.indexOf(":" + el_obj.value + ":") >= 0)
          {
            el_obj.checked = true;
          }
        }
      }
    }
    else
    {
      if (fm_obj.elements[cook_name] != void(0) && ltu_get_obj_fld_value2(fm_obj, cook_name) == "")
      {
        ltu_set_obj_fld_value2(fm_obj, cook_name, cook_value);
      }
    }
  }
}

// set defaults fields add to work string
function ltu_setdef_fld_to_wstr(fm_obj, fld_name, wstr)
{
  obj_val = "";
  if (fld_name.indexOf("[]") >= 0)
  {
    obj_val += ":";
    for(i = 0; i < fm_obj.elements.length; i ++)
    {
      el_obj = fm_obj.elements[i];
      if (el_obj.name == fld_name && el_obj.checked) { obj_val += el_obj.value + ":"; }
    }
  }
  else
  {
    obj_val = ltu_get_obj_fld_value2(fm_obj, fld_name);
  }
  wstr += fld_name + "\t" + obj_val + "\t";
  return wstr;
}

// set defaults work string to cookie
function ltu_setdef_wstr_to_cookie(cookie_name, wstr)
{
  ltu_set_cookie(cookie_name, wstr);
}

// from java to php encode
function ltu_to_php_encode(p_str)	// (R) return
{
  return encodeURIComponent(p_str);
}

// from php to java decode
function ltu_from_php_decode(p_str)	// (R) return
{
  return decodeURIComponent(p_str);
}

// ajax
function ltu_ajax_exec(	// (R) return
  p_type,		// (I) GET / POST
  p_url,		// (I) url
  p_data)		// (I) post data
{
  var p_rtn = "";

  // create
  var xmlhttp = ltu_ajax_create_xml_http();
  if (xmlhttp == null)
  {
    p_rtn = "XMLHttpRequest非対応のブラウザです。";
    return p_rtn;
  }

  // ブラウザ判定
  var ua        = navigator.userAgent;
  var safari	= ua.indexOf("Safari") != -1;
  var konqueror = ua.indexOf("Konqueror") != -1;
  var mozes	    = ( (a=ua.split("Gecko/")[1] ) ? a.split(" ")[0] : 0 ) >= 20011128;

  // status change callback
  // operaはonreadystatechangeに多重レスバグがあるのでonloadが安全
  // Moz,FireFoxはoj.readyState==3でも受信するので通常はonloadが安全
  // Win ieではonloadは動作しない
  // Konquerorはonloadが不安定
  // 参考http://jsgt.org/ajax/ref/test/response/responsetext/try1.php
  if (window.opera || safari || mozes)
  {
    xmlhttp.onload = function()
    {
      if (xmlhttp.readyState == 4)
      {
        if (xmlhttp.status == 200) { p_rtn = xmlhttp.responseText; }   // get response
        else                       { p_rtn = "通信エラーが発生しました。"; }
      }
    }
  }
  else
  {
    xmlhttp.onreadystatechange = function()
    {
      if (xmlhttp.readyState == 4)
      {
        if (xmlhttp.status == 200) { p_rtn = xmlhttp.responseText; }   // get response
        else                       { p_rtn = "通信エラーが発生しました。"; }
      }
    }
  }

  // open
  xmlhttp.open(p_type, p_url, false);	// true 非同期 / false 同期

  // send and wait
  if (p_type == "POST" || p_type == "post")
  {
    var p_post_data = "";
    var p_joi       = "";
    for (p_key in p_data)
    {
      //var p_val   = encodeURI(p_data[p_key]).replace(/&/g , "%26");
      var p_val   = ltu_to_php_encode(p_data[p_key]);
      p_post_data = p_post_data + p_joi + p_key + "=" + p_val;
      p_joi       = "&";
    }
    xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded; charset=UTF-8");
    xmlhttp.send(p_post_data);
  }
  else
  {
    xmlhttp.send(null);
  }

  return ltu_from_php_decode(p_rtn);
}

function ltu_ajax_create_xml_http()
{
  if (window.XMLHttpRequest) // Mozilla, Firefox, Safari, IE7
  {
    return new XMLHttpRequest();
  }
  else if (window.ActiveXObject) // IE5, IE6
  {
    try
    {
      return new ActiveXObject("Msxml2.XMLHTTP");    // MSXML3
    }
    catch(e)
    {
      return new ActiveXObject("Microsoft.XMLHTTP"); // MSXML2
    }
  }
  else
  {
    return null;
  }
}

