
INSERT INTO PALLET_TYPE (ID, CODE, NAME, OLDPALLETTYPE, PREFIX, PROCWARESCHK, CANMOVE, PROCREFILLCHK, WARESID_PALLET, MINGENID, MAXGENID, SERIES, PREFIXNUM, PALNUMLENGTH) VALUES (11, 'CR', '������ ������� ��������� �� ��������', 'C', 'C', NULL, '1', '0', NULL, 1, 99999, 1, 'C', 5);

UPDATE WM_CONFIG W
   set w.objid_whreject = (select first(1) oi.objid from wh_obj_info oi);


INSERT INTO SITEOPTION (CODE, NAME, WITHCHILDREN) VALUES ('COMERETURN', '�������������� ���� ���������', '1');


INSERT INTO DOCTYPEOBJ (DOCTID, NUMOBJ, OBJCATID, ISOWNER, OBJID, CANCHOICE, REQUIRED, ISCOMPANY, ISMAN, ISDEPART, WARESRESTCHANGE, WARESCIRCTYPE, CHECKWARESREST, MONEYRESTCHANGE, MONEYCIRCTYPE, CHECKMONEYREST, CAPTION, SESSIONID, LASTDATE, MONEYNUMOBJ2, RESTCHECK, RESTAMOUNTCHECK, OBJFILTID, OBJSTATUSES, WARESLOTTYPE, NUM, WARESRESTTYPE, MONEYRESTTYPE, ISOBJZONE, ISOBJRESERVE) VALUES (4, '1', NULL, '0', NULL, '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '������', NULL, '4-NOV-2016 22:14:25', NULL, '2', '0', NULL, NULL, NULL, 1, '0', '0', NULL, 's');