#!/usr/bin/python

def command_parse(args=None):
    """ Parsing command-line arguments """
    from argparse import RawTextHelpFormatter
    import argparse
    parser = argparse.ArgumentParser(description="(Mysql,RAW_) to (vasp,wien2k,cif)",
                                     add_help=False,
                                     formatter_class=RawTextHelpFormatter)
    parser.set_defaults()
    #Group
    in_parser = parser.add_argument_group("##########Input##########")
    out_parser = parser.add_argument_group("##########Output##########")
    #in_format
    in_parser.add_argument("--in_format","-if",
                             required=True,
                             help="""\
    [uuid,raw]
                                  """)
    #inpath
    in_parser.add_argument("--inpath","-i",
                             help="""\
    (UUID num) for case of --in_format uuid,default=""
    (path) for case of --in_format raw,default="./RAW_*"
                                  """)
    #out_format
    out_parser.add_argument("--out_format","-of",
                             default="cif",
                             help="""\
    [vasp-a,vasp-w,wien2k-a,wien2k-w,cif,cif-a] default="cif"
    __-a:transform by ase
    __-w:transform by wien2pos(ase-fix)
                                  """)
    #outpath
    out_parser.add_argument("--outpath","-o",
                             metavar="path",
                             help="""\
    default=["./POSCAR_(UUID num or *)",
         "./struct_(UUID num or *)",
         "./(UUID num or *).cif"]
                                  """)

    out_parser.add_argument("--IDNUM","-id",nargs='?',default="nobug")

#    #help
    parser.add_argument("-h", "--help", action="help",
                        help="show this help message and exit")
    if args is None:
        ret = vars(parser.parse_args())
    else:
        ret = vars(parser.parse_args(args.split()))
    return ret

def out_part(out_format,outpath,inpath,
                        UUID,
                        From,
                        IDNUM,
                        name,
                        sgrnum,
                        sgr,
                        cellpar,
                        modif,
                        sgrlc,
                        elemd,
                        ele,
                        basis,
                        elecount,
                        wycsym,
                        occup,
                        doping,
                        symreco,
                        z_count,
                        el_kinds,
                        c_vol,
                        r_val,
                        ox,
                        hy,
                        itf,
                        atom_symb_num,
                        ox_ele,
                        ox_state,
                        ccode):
#    print out_format[:-2]
    if out_format[:-2] == 'vasp' and outpath == None:
        outpath = doping+'POSCAR_'+str(inpath)
    elif out_format[:-2] == 'wien2k' and outpath == None:
        outpath = doping+'struct_'+str(inpath)
    elif out_format[:3] == 'cif' and outpath == None:
        outpath = doping+str(inpath + ".cif")
     #print out_format[-2:]
    from lib.transProgram import CL_output
    clout=CL_output()
    cCb=clout.CHECK_basis(elecount,ele,basis)
    if cCb==True:
        print 'UUID='+str(UUID)+' Database Wyckoff Symbol Positions Missing, Not Output File.'
        return 1
    elif cCb==False:
        if out_format == 'cif':
            clout.OUT_cif(outpath,
                      UUID,
                      cellpar,
                      sgr,
                      sgrnum,
                      elecount,
                      ele,
                      wycsym,
                      basis,
                      occup,
                      symreco,
                      c_vol,
                      r_val,
                      z_count,
                      ox,
                      hy,
                      itf,
                      atom_symb_num,
                      ox_ele,
                      ox_state,
                      ccode)
        elif out_format[-2:] == '-w':
            clout.OUT_wien2pos(outpath,
                               cellpar,
                               sgrlc,
                               sgrnum,
                               elecount,
                               ele,
                               basis,
                               out_format[:-2],
                               UUID)
        elif out_format[-2:] == '-a':
            run_ase_a='clout.OUT_ase_'+str(out_format[:-2])
            eval(run_ase_a)(outpath,
                            cellpar,
                            sgrnum,
                            elecount,
                            ele,
                            basis,
                            UUID)
def MAIN_OUT2file(args=None): 
    opts = command_parse(args)
    if opts['in_format']=='uuid':
        from lib.Readinfo import CL_read_info
        info=CL_read_info()
        info.get_sql_data('UUID='+opts["inpath"])
        if opts['IDNUM']!="nobug":
            print info.INFO_IDNUM
        inpath=opts['inpath']
        out_format=opts['out_format']
        outpath=opts['outpath']
        o_p=out_part(out_format,
                 outpath,
                 inpath,
                 info.INFO_UUID,
                 info.INFO_from,
                 info.INFO_IDNUM,
                 info.INFO_name,
                 info.INFO_sgrnum,
                 info.INFO_sgr,
                 info.INFO_cellpar,
                 info.INFO_modif,
                 info.INFO_sgrlc,
                 info.INFO_elemd,
                 info.INFO_ele,
                 info.INFO_basis,
                 info.INFO_elecount,
                 info.INFO_wycsym,
                 info.INFO_occup,
                 info.INFO_doping,
                 info.INFO_symreco,
                 info.INFO_z_count,
                 info.INFO_el_kinds,
                 info.INFO_c_vol,
                 info.INFO_r_val,
                 info.INFO_ox,
                 info.INFO_hy,
                 info.INFO_itf,
                 info.INFO_atom_symb_num,
                 info.INFO_ox_ele,
                 info.INFO_ox_state,
                 info.INFO_ccode)
        return o_p
    elif opts['in_format']=='raw':
        from lib.Readinfo import CL_read_info
        info=CL_read_info()
        if opts['inpath']==None:
            import os
            RAW_name=[]
            RAW_li= os.listdir('.')
            for key in RAW_li:
                if key.find('RAW_') == 0:
                    RAW_name.append(key)
            for raw in RAW_name:
                info.get_raw_data(raw)
                inpath=raw[4:]
                out_format=opts['out_format']
                outpath=opts['outpath']
                out_part(out_format,
                         outpath,
                         inpath,
                         info.INFO_UUID,
                         info.INFO_from,
                         info.INFO_IDNUM,
                         info.INFO_name,
                         info.INFO_sgrnum,
                         info.INFO_sgr,
                         info.INFO_cellpar,
                         info.INFO_modif,
                         info.INFO_sgrlc,
                         info.INFO_elemd,
                         info.INFO_ele,
                         info.INFO_basis,
                         info.INFO_elecount,
                         info.INFO_wycsym,
                         info.INFO_occup,
                         info.INFO_doping,
                         info.INFO_symreco)
        elif opts['inpath']!=None:
            info.get_raw_data(opts['inpath'])
            if opts['inpath'][:4]=='RAW_':
                inpath=opts['inpath'][4:]
            out_format=opts['out_format']
            outpath=opts['outpath']
            out_part(out_format,
                     outpath,
                     inpath,
                     info.INFO_UUID,
                     info.INFO_from,
                     info.INFO_IDNUM,
                     info.INFO_name,
                     info.INFO_sgrnum,
                     info.INFO_sgr,
                     info.INFO_cellpar,
                     info.INFO_modif,
                     info.INFO_sgrlc,
                     info.INFO_elemd,
                     info.INFO_ele,
                     info.INFO_basis,
                     info.INFO_elecount,
                     info.INFO_wycsym,
                     info.INFO_occup,
                     info.INFO_doping,
                     info.INFO_symreco)
