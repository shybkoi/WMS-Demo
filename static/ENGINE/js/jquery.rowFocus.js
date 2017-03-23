(function(jQuery){var rfnoFocusClass='rf-nofocus';var rfSelectClass='rowSelect';var rfFocusClass='rf-focused';var rfFocusClassLast='rf-focused-last';jQuery.fn.rowFocus=function(rfoptions)
{var rfoptions=jQuery.extend({rfbody:'tbody',rfFocusCallBack:null,rfSetDefFocus:true,rfMultiSelect:false,rfScrolling:false,rfNewFocusClass:false},rfoptions);if(rfoptions.rfNewFocusClass)rfFocusClass=rfoptions.rfNewFocusClass;return this.each(function()
{function rfHasSelected(row)
{if(jQuery(row).hasClass(rfFocusClass)||jQuery(row).hasClass(rfnoFocusClass)||jQuery(row).hasClass(rfFocusClassLast))return true;else return false;};function rfSetFocus(row)
{if(jQuery(row).hasClass(rfSelectClass))jQuery(row).addClass(rfFocusClassLast);else jQuery(row).addClass(rfFocusClass);if(!jQuery(row).attr("id"))jQuery(row).attr('id',rfFocusClass);return true;};function rfSelect(row)
{if(rfHasSelected(row))return false;rfClearFocus(jQuery(row).parents("table"));rfSetFocus(row);return true;};function rfTrigger(row)
{if(rfSelect(row)){if(rfoptions.rfFocusCallBack)rfoptions.rfFocusCallBack.apply(row,arguments)};};function rfGetRows($el)
{if($el.is("table"))
return jQuery(rfoptions.rfbody+' tr',$el);if($el.is("tbody"))
return jQuery('tr',$el);if($el.is("tr"))
return $el;}
if(rfoptions.rfMultiSelect)
{rfGetRows(jQuery(this)).unbind(rfoptions.rfMultiSelect).unbind('rightMouseDown').bind(rfoptions.rfMultiSelect,function()
{var $tr=$(this);if($tr.hasClass(rfSelectClass))
{if($tr.hasClass(rfFocusClassLast))$tr.removeClass(rfFocusClassLast).addClass(rfFocusClass);}
else
{if($tr.hasClass(rfFocusClass))$tr.removeClass(rfFocusClass).addClass(rfFocusClassLast);}
$tr.toggleClass(rfSelectClass);if(rfoptions.rfFocusCallBack)rfoptions.rfFocusCallBack.apply($tr,arguments);}).rightMouseDown(function(){rfTrigger(this);})}
else
rfGetRows(jQuery(this)).unbind('click').unbind('rightMouseDown').click(function(){rfTrigger(this);}).rightMouseDown(function(){rfTrigger(this);});if(rfoptions.rfSetDefFocus)
{var firstrow=rfGetRows(jQuery(this)).filter(":first");if(firstrow)
{if(rfoptions.rfMultiSelect)jQuery(firstrow).trigger("rightMouseDown");else jQuery(firstrow).click();}}});};function rfClearFocus(_tbl_)
{var row=jQuery(_tbl_).find('tr.'+rfFocusClass);if(row.length==0)
row=jQuery(_tbl_).find('tr.'+rfFocusClassLast);row.removeClass(rfFocusClass).removeClass(rfFocusClassLast);if(jQuery(row).attr("id")==rfFocusClass)jQuery(row).removeAttr('id');};jQuery.fn.rfGetFocus=function()
{var $rf=jQuery(this).find("tr."+rfFocusClass);if($rf.length==1)return $rf.attr("id");var $rf=jQuery(this).find("tr."+rfFocusClassLast);if($rf.length==1)return $rf.attr("id");return'';};jQuery.fn.rf$GetFocus=function()
{var $rf=jQuery(this).find("tr."+rfFocusClass);if($rf.length==1)return $rf;return jQuery(this).find("tr."+rfFocusClassLast);};jQuery.fn.rfIsFocus=function(){return jQuery(this).hasClass(rfFocusClass);};jQuery.fn.rfSetFocus=function(row,isevent)
{if(row){rfClearFocus(this);isevent!==false?jQuery(row).click():jQuery(row).addClass(rfFocusClass);}
else{if(this.is("tr")){rfClearFocus(this.parents("table:first"));isevent!==false?this.click():this.addClass(rfFocusClass);}}
return this;};jQuery.fn.rfGetSelect=function(){return jQuery("tbody>tr."+rfSelectClass,this);};jQuery.fn.rfSetSelect=function()
{return this.each(function()
{var $tr=jQuery(this);if(!$tr.hasClass(rfSelectClass))
{$tr.addClass(rfSelectClass);if($tr.hasClass(rfFocusClass))$tr.removeClass(rfFocusClass).addClass(rfFocusClassLast);}});};jQuery.fn.rfDelSelect=function()
{return this.each(function()
{var $tr=jQuery(this);if($tr.hasClass(rfSelectClass))
{$tr.removeClass(rfSelectClass);if($tr.hasClass(rfFocusClassLast))$tr.removeClass(rfFocusClassLast).addClass(rfFocusClass);}});};})(jQuery);