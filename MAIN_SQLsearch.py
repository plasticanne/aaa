#!/usr/bin/python

def logic_parse(args=None):
    """ Parsing command-line arguments """
    from argparse import RawTextHelpFormatter
    import argparse
    parser = argparse.ArgumentParser(description="Search infomation from SQL",
                                     add_help=False,
                                     formatter_class=RawTextHelpFormatter)
    parser.set_defaults()
    #Group
    logi_parser = parser.add_argument_group("##########Search Logic##########")
    rules_parser = parser.add_argument_group("##########Search Rules##########")
    example_parser = parser.add_argument_group("##########Example##########")
    output_parser = parser.add_argument_group("##########Output##########")
    #logic
    logi_parser.add_argument("logic:",nargs='?',help="""\
                                  """)
    #and
    logi_parser.add_argument("--and","-&",\
                             help="""\
    search intersection of the rules
    put rules inside "" 
    example --and "--rules [...]"
                                  """)
    #or
    logi_parser.add_argument("--or","-|",\
                             help="""\
    search union of the rules
    put rules inside ""
    example --or "--rules [...]"
                                  """)
    #not
    logi_parser.add_argument("--not","-n",\
                             help="""\
    search difference sets of the rules
    put rules inside ""
    example --not "--rules [...]"
                                  """)
    #Example
    example_parser.add_argument("example:",nargs='?',\
                             help="""\
--and "--ele Na2,Cl1,O# --sgn 15" 
--or "--ele Bi#,C2" --not "--ele O2"
Will find out all results :

   SG15,   Na2,Cl1 with O1,O3,O4...
or SG15,C2,Na2,Cl1 with O1,O3,O4...
or SG15,   Na2,Cl1 with O1,O3,O4... with Bi1,Bi2,Bi3...

                                  """)
    #rules
    rules_parser.add_argument("rules:",nargs='?',
                             help="""\
                                  """)
    #element 
    rules_parser.add_argument("--ele","-e",\
                             help="""\
    kinds of elemants
    'Xx' for an any atom
    '#' for any number of atoms
    set format --ele Na2,Cl2 or Na#,Cl2 for unknow number Na
    Dont wtite like (NaCl)2 or (Na2,Cl2) 
                                  """)
#    #element number
#    rules_parser.add_argument("--num","-#",\
#                             help="""\
#    number of each elemant
#    set list --num [Na2,Cl2]
#    Dont wtite like (NaCl)2 or (Na2,Cl2) or "Na2,Cl2"
#                                  """)

    #space group number
    rules_parser.add_argument("--sgn","-s",\
                             help="""\
    space group number 
                                  """)

    #Coll code
    rules_parser.add_argument("--ccode","-cc",\
                             help="""\
    Coll code
                                  """)
    #output
    output_parser.add_argument("--comment","-com",nargs='?',default="nobug",\
                             help="""\
    show comments
                                  """)

    #output
    output_parser.add_argument("--out_format","-of",\
                             help="""\
    [vasp-a,vasp-w,wien2k-a,wien2k-w,cif,cif-a]
    __-a:transform by ase
    __-w:transform by wien2pos(ase-fix)
                                  """)
    #outpath
    output_parser.add_argument("--outpath","-o",\
                             metavar="path",\
                             help="""\
    folder path for output
    default=["./POSCAR_(UUID num or *)",
             "./struct_(UUID num or *)",
             "./(UUID num or *).cif"]
                                  """)

#    #help
    parser.add_argument("-h", "--help", action="help",\
                        help="""show this help message and exit\



                             """)
    if args is None:        
        ret = vars(parser.parse_args())
    else:
#        print args.split('<>')
        ret = vars(parser.parse_args((args.split("<>"))))
#    print ret
    and_arg=ret['and']
    or_arg=ret['or']
    not_arg=ret['not']
    of_arg=ret['out_format']
    o_arg=ret['outpath']
    com_arg=ret['comment']
#    print and_arg
#    print or_arg
#    print not_arg
#    print of_arg
    if and_arg!=None:
        and_ret = vars(parser.parse_args(and_arg.split()))
    elif and_arg==None:
        and_ret = None
    if or_arg!=None:
        or_ret = vars(parser.parse_args(or_arg.split()))
    elif or_arg==None:
        or_ret = None
    if not_arg!=None:
         not_ret = vars(parser.parse_args(not_arg.split()))
    elif not_arg==None:
        not_ret = None
    return and_ret,or_ret,not_ret,of_arg,o_arg,com_arg

###and###
def logic_and_to_sql(ele,sgn,ccode):
    and_ccode=""
    if ele==[]:
        and_ele=""
        and_ele_count=""
        if sgn!=None:
            and_sgn=" join ( select UUID_IDNUM.UUID,ICSD_ALL.SGR_NUM from UUID_IDNUM \
                    inner join ICSD_ALL using(IDNUM) where SGR_NUM="+str(sgn)+") as A0 using (UUID) "
        elif sgn==None:
            and_sgn=""
            and_ccode=" join ( select UUID_IDNUM.UUID,ICSD_ALL.COLL_CODE from UUID_IDNUM \
                    inner join ICSD_ALL using (IDNUM) where COLL_CODE="+str(ccode)+" ) as A0 using (UUID) "

    elif ele!=[]:
        and_ele="" 
        for i in range(len(ele)):
            if ele[i][0]=='Xx':    
                if ele[i][1]=='#':
                    and_ele_num=""
                elif ele[i][1]!='#':
                    and_ele_num=" where EL_SUBSCRIPT="+ele[i][1]
                and_ele=and_ele+" join (select UUID_IDNUM.UUID,ICSD_ELEMENT.EL_SYMBOL from UUID_IDNUM \
                                 inner join ICSD_ELEMENT using(IDNUM) "\
                               +and_ele_num\
                               + ") as A" + str(i) + " using (UUID) "
            if ele[i][0]!='Xx':
                if ele[i][1]=='#':
                    and_ele_num=""
                elif ele[i][1]!='#':
                    and_ele_num=" and EL_SUBSCRIPT="+ele[i][1]
                and_ele=and_ele+" join (select UUID_IDNUM.UUID,ICSD_ELEMENT.EL_SYMBOL from UUID_IDNUM \
                                 inner join ICSD_ELEMENT using(IDNUM) where EL_SYMBOL='"\
                               + ele[i][0] +"'"\
                               +and_ele_num\
                               + ") as A" + str(i) + " using (UUID) "

        and_ele_count=" join (select UUID_IDNUM.UUID,ICSD_ELEMENT.EL_SYMBOL from UUID_IDNUM \
                       inner join ICSD_ELEMENT using(IDNUM) \
                       group  by IDNUM having count(*)=" +str(len(ele))+ ") as B using (UUID) "
        if sgn == None:
            and_sgn=""
        elif sgn != None:
            and_sgn=" join ( select UUID_IDNUM.UUID,ICSD_ALL.SGR_NUM from UUID_IDNUM \
                      inner join ICSD_ALL using(IDNUM) where SGR_NUM="+str(sgn)+") as C using (UUID) "

    return and_ele,and_ele_count,and_sgn,and_ccode

###not###
def logic_not_to_sql(ele,sgn):
    not_eleD=[]
    for i in range(len(ele)):
        if ele[i][0]=='Xx':
            if ele[i][1]=='#':
                not_ele_num=""
            elif ele[i][1]!='#':
                not_ele_num="where EL_SUBSCRIPT="+ele[i][1]
            not_eleD.append("UUID not in (select UUID_IDNUM.UUID  from UUID_IDNUM \
                         inner join ICSD_ELEMENT using(IDNUM) "\
                       +not_ele_num\
                       + ")")
        if ele[i][0]!='Xx':
            if ele[i][1]=='#':
                not_ele_num=""
            elif ele[i][1]!='#':
                not_ele_num=" and EL_SUBSCRIPT="+ele[i][1]
            not_eleD.append("UUID not in (select UUID_IDNUM.UUID  from UUID_IDNUM \
                         inner join ICSD_ELEMENT using(IDNUM) where EL_SYMBOL='"\
                       + ele[i][0] +"'"\
                       +not_ele_num\
                       + ")")
    if not_eleD==[]:
        not_ele=""
    elif not_eleD!=[]:
        not_eleD_in=""
        for i in range(1,len(not_eleD)):
            not_eleD_in=not_eleD_in+" and "+not_eleD[i]
        not_ele="where "+not_eleD[0]+not_eleD_in
    if sgn == None:
        not_sgn=""
    elif sgn != None:
        not_sgn="join ( select UUID_IDNUM.UUID,ICSD_ALL.SGR_NUM from UUID_IDNUM  \
                 inner join ICSD_ALL using(IDNUM) where SGR_NUM<>"+str(sgn)+") as D using (UUID)"
    return not_sgn,not_ele
    

###or###
SQL_view=''
def logic_or_to_sql(or_sgn,and_ele,or_ele,and_sgn,l_not_ele,l_not_sgn,ccode):
    if or_sgn==None:
        tosql_1=""
    elif or_sgn!=None:
        l_and_or_sgn=logic_and_to_sql(and_ele,or_sgn,ccode)
        tosql_1=" UNION "+str(\
        "Select A0.UUID,ICSD_ALL.SUM_FORM,ICSD_ALL.SGR_NUM,ICSD_ALL.Z,ICSD_ALL.A_LEN,ICSD_ALL.B_LEN,ICSD_ALL.C_LEN,ICSD_ALL.ALPHA,ICSD_ALL.BETA,ICSD_ALL.GAMMA,ICSD_ALL.IDNUM,ICSD_ALL.COLL_CODE from UUID_IDNUM  \
         inner join   ICSD_ALL  using (IDNUM)"\
         +l_and_or_sgn[0]\
         +l_and_or_sgn[1]\
         +l_and_or_sgn[2]\
         +l_not_ele\
         +l_not_sgn\
         )
    tosql_2=""
    tosql_2_sgn=""
    for i in range(len(or_ele)):
        and_or_ele=[]
        and_or_ele.extend(and_ele)
        and_or_ele.append(or_ele[i])
        l_and_or_ele=logic_and_to_sql(and_or_ele,and_sgn)
        tosql_2=tosql_2+" UNION "+str(\
                "Select A0.UUID,ICSD_ALL.SUM_FORM,ICSD_ALL.SGR_NUM,ICSD_ALL.Z,ICSD_ALL.A_LEN,ICSD_ALL.B_LEN,ICSD_ALL.C_LEN,ICSD_ALL.ALPHA,ICSD_ALL.BETA,ICSD_ALL.GAMMA,ICSD_ALL.IDNUM.COLL_CODE from UUID_IDNUM  \
                inner join   ICSD_ALL  using (IDNUM)"\
                +l_and_or_ele[0]\
                +l_and_or_ele[1]\
                +l_and_or_ele[2]\
                +l_not_ele\
                +l_not_sgn\
                )
        if or_sgn==None:
            tosql_2_sgn=""
        elif or_sgn!=None:
            l_and_or_ele_sgn=logic_and_to_sql(and_or_ele,or_sgn)
            tosql_2_sgn=tosql_2_sgn+" UNION "+str(\
                        "Select A0.UUID,ICSD_ALL.SUM_FORM,ICSD_ALL.SGR_NUM,ICSD_ALL.Z,ICSD_ALL.A_LEN,ICSD_ALL.B_LEN,ICSD_ALL.C_LEN,ICSD_ALL.ALPHA,ICSD_ALL.BETA,ICSD_ALL.GAMMA,ICSD_ALL.IDNUM,ICSD_ALL.COLL_CODE from UUID_IDNUM  \
                        inner join   ICSD_ALL  using (IDNUM)"\
                        +l_and_or_ele_sgn[0]\
                        +l_and_or_ele_sgn[1]\
                        +l_and_or_ele_sgn[2]\
                        +l_not_ele\
                        +l_not_sgn\
                        )
    return tosql_1,tosql_2,tosql_2_sgn




def MAIN_SQLsearch(args=None):
    logic=logic_parse(args)
    import re
    logicD=[]
#    print logic[0]
    for logic_n in range(0,3):
        if logic[logic_n]==None:
            eleD=[]
            sgn=None
            ccode=None
        elif logic[logic_n]!=None:
            ccode=logic[logic_n]['ccode']
            sgn=logic[logic_n]['sgn']
            if logic[logic_n]['ele']==None:
                eleD=[]
            elif logic[logic_n]['ele']!=None:
                eleD=[]
                for i in range(len(logic[logic_n]['ele'].split(","))):
                    eleD.append([re.findall("[A-Z][a-z]|[A-Z]",\
                                (logic[logic_n]['ele'].split(","))[i])[0],\
                                 re.findall("[0-9][0-9][0-9]|[0-9][0-9]|[0-9]|['#']",\
                                (logic[logic_n]['ele'].split(","))[i])[0]])
        logicD.append([eleD,sgn,ccode])

    

    l_and=logic_and_to_sql(logicD[0][0],logicD[0][1],logicD[0][2])
    l_not=logic_not_to_sql(logicD[2][0],logicD[2][1])
    l_or=logic_or_to_sql(logicD[1][1],logicD[0][0],logicD[1][0],logicD[0][1],l_not[0],l_not[1],logicD[0][2])
    if logic[5]=='nobug':
        show_comments=''
        tag_comments=''
    elif logic[5]!='nobug':
        show_comments="join ( select UUID_IDNUM.UUID,ICSD_COMMENTS.COMMENTS from UUID_IDNUM \
                      left join ICSD_COMMENTS using(IDNUM) ) as F using (UUID) "
        tag_comments=',F.COMMENTS'
    from dbhost import cl_db_host
    cldbhost=cl_db_host()
    cursor = cldbhost.db.cursor()
    cursor.execute(\
#    "Select A0.UUID,ICSD_ALL.SUM_FORM,ICSD_ALL.SGR_NUM from UUID_IDNUM  inner join   ICSD_ALL  using (IDNUM)"\
    "Select A0.UUID,ICSD_ALL.SUM_FORM,ICSD_ALL.SGR_NUM,ICSD_ALL.Z,ICSD_ALL.A_LEN,ICSD_ALL.B_LEN,ICSD_ALL.C_LEN,ICSD_ALL.ALPHA,ICSD_ALL.BETA,ICSD_ALL.GAMMA,ICSD_ALL.IDNUM,ICSD_ALL.COLL_CODE"+tag_comments+ " from UUID_IDNUM  inner join   ICSD_ALL  using (IDNUM)"\
    +l_and[0]\
    +l_and[1]\
    +l_and[2]\
    +l_and[3]\
    +l_not[0]\
    +l_not[1]\
    +l_or[0]\
    +l_or[1]\
    +l_or[2]\
    +show_comments\
    +";")
    result = cursor.fetchall()


    for i in range(len(result)):
        if logic[5]=='nobug':
            out_comments=''
        elif logic[5]!='nobug':
            out_comments='\n     Comments: '+str(result[i][12])

        if result[i][0]==result[i-1][0] and i!=0:
            print out_comments,
        else:
            print "\n\n[[ "+str(result[i][1])+" ]]"+"\n     UUID: "+str(result[i][0])+"    SG NUM: "+str(result[i][2])+"    Z: "+str(result[i][3])+"    IDNUM: "+str(result[i][10])+"    COLL CODE: "+str(result[i][11])+\
            '\n     (a,b,c,alpha,beta,gamma): ('+str(result[i][4])+' , '+str(result[i][5])+' , '+str(result[i][6])+' , '+str(result[i][7])+' , '+str(result[i][8])+' , '+str(result[i][9])+')'+out_comments,
        if logic[3] !=None:
            if logic[4] ==None:
                from lib.MAIN_OUT2file import MAIN_OUT2file
                uuid=result[i][0]
                MAIN_OUT2file(" --in_format uuid --inpath "+str(uuid)+ " --out_format "+str(logic[3]))
            if logic[4] !=None:
                import os
                cwd=os.getcwd()      
                os.chdir(logic[4])
                from lib.MAIN_OUT2file import MAIN_OUT2file
                uuid=result[i][0]
                MAIN_OUT2file(" --in_format uuid --inpath "+str(uuid)+ " --out_format "+str(logic[3]))
                os.chdir(cwd)
