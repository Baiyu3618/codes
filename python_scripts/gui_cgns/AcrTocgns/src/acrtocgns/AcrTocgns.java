package acrtocgns;

import java.io.* ;
import java.util.* ;
import com.acri.utils.* ;
import com.acri.dataset.* ;

import com.acri.cgns.* ;
import com.acri.mergeDataSet.gui.DatasetLoadUtilities;


public class AcrTocgns {
        
    // member variables.
    protected String _fileName = "" ;
    protected SWIGTYPE_p_int _cgfile = CGNS.new_intp() ;

    protected String _base = "Unstructured data" ;
    protected SWIGTYPE_p_int _baseIndex = CGNS.new_intp() ;

    protected String _zone = "fluid" ;
    protected SWIGTYPE_p_int _zoneIndex = CGNS.new_intp() ;

    protected SWIGTYPE_p_int _xcIndex = CGNS.new_intp() ;
    protected SWIGTYPE_p_int _ycIndex = CGNS.new_intp() ;
    protected SWIGTYPE_p_int _zcIndex = CGNS.new_intp() ;

    protected int _ierror = 0 ;
    protected String _errMsg = "" ;
    // member variables.
    
    static {
        System.loadLibrary( "acri_cgns_x64" ) ;
    }

    protected AcrTocgns() {
    } // end of constructor TestCGNS01 (default).

    public void setFileName(String fileName) { _fileName = fileName ; }
    public void setBaseName(String name) { _base = name ; }
    public void setZoneName(String name) { _zone = name ; }

    public void checkError() throws IOException {
        _errMsg = "" ;
        if( _ierror > 0 ) {
            _errMsg = CGNS.cg_get_error() ;
            System.err.println( _errMsg ) ;
            throw new IOException( "CGNS Error" + _errMsg ) ;
        }
    } // end of method checkError

    protected void cg_open_for_write( DataSet d ) throws IOException {
        _ierror = CGNS.cg_open( _fileName, CGNS.CG_MODE_WRITE, _cgfile ) ;
        checkError() ;

        // Write base
        final int celldim  = d.getDim() ;
        final int phydim = celldim ;
        final int c = CGNS.intp_value( _cgfile ) ;
//        System.out.println("dim : " + celldim + " pdim : " + phydim);
        _ierror = CGNS.cg_base_write(c, _base, celldim, phydim, _baseIndex ) ;
        checkError() ;
    } // end of method cg_open_for_write

    protected void cg_close() throws IOException {
        _ierror = CGNS.cg_close( CGNS.intp_value( _cgfile ) ) ;
        checkError() ;
        if( _ierror > 0 ) throw new IOException( "CGNS File Close Error" + _errMsg ) ;
    } // end of method cg_close

    public void writeGrid( DataSet d ) throws IOException, RegionException, AcrException {
        // Write Zone
        final int c = CGNS.intp_value( _cgfile ) ;
        final int b = CGNS.intp_value( _baseIndex ) ;

        ZoneType_t zoneType = ZoneType_t.Unstructured ;
        SWIGTYPE_p_int size = CGNS.new_intArray(3) ;

        final int nverts = d.getNumberOfVertices() ;
        final int nfld   = d.getNumberOfCells() ;
        final int nmax   = d.getNumberOfNodes() ;

        CGNS.intArray_setitem( size, 0, nverts ) ;
        CGNS.intArray_setitem( size, 1, nfld ) ;
        CGNS.intArray_setitem( size, 2, 0 ) ; // elements not sorted.
        
        _ierror = CGNS.cg_zone_write( c, b, _zone, size, zoneType, _zoneIndex ) ;   
        checkError() ;

        // write coordinates.
        final int iz = CGNS.intp_value( _zoneIndex ) ;
        DataType_t rd = DataType_t.RealDouble ;
        String cName = "" ;

        // X
        SWIGTYPE_p_void xc = CGNS2.doubleArray2( d.getXC() ) ;
        cName = "CoordinateX" ;
        _ierror = CGNS.cg_coord_write( c,b,iz,rd,cName, xc, _xcIndex );
        checkError() ;

        // Y
        SWIGTYPE_p_void yc = CGNS2.doubleArray2( d.getYC() ) ;
        cName = ( d.isCylindrical() ? "CoordinateR" : "CoordinateY" ) ;
        _ierror = CGNS.cg_coord_write( c,b,iz,rd,cName, yc, _ycIndex );
        checkError() ;
       
        // Z
        if( d.is3D() ) {
            SWIGTYPE_p_void zc = CGNS2.doubleArray2( d.getZC() ) ;
            cName = ( d.isCylindrical() ? "CoordinateTheta" : "CoordinateZ" ) ;
            _ierror = CGNS.cg_coord_write( c,b,iz,rd,cName, zc, _zcIndex );
            checkError() ;
        }
    
        // write element connectivity section
        int[] m2tx = d.getM2TX(); //Element type
        int[] m2cx = d.getM2CX(); // number of vertex for each element
        int[] m2cc = d.getM2CC(); // offset into vertex connectivity
        int[] lcrn = d.getVertexData(); // vertex connectivity for elements.
        
        SWIGTYPE_p_int cell_section_index = CGNS.new_intp();
        
        int nele_start = 0;
        int nele_end = nfld - 1;
        int nbdyelement = 0;
        final int total_length = m2cc[nfld] + m2tx.length;
//        System.out.println("Total length : " + total_length + " lcrn : " + lcrn.length + " m2tx : " + m2tx.length);
        SWIGTYPE_p_int vtxList = CGNS.new_intArray(total_length);

        int count = 0;
        for(int e = 0; e < nfld; e++){
            final int nv = m2cx[e];
            final int offset = m2cc[e];
//            System.out.println("Cell " + e + " : " + "No. vrtx : " + nv + " " + "offset : " + offset);
            final int acrCellType = m2tx[e];
            CGNS.intArray_setitem(vtxList, count, getCGNSCellType(acrCellType, nv));
            count++;
            for(int v = 0; v < nv; v++){
                int index = offset + v;
                final int vn = lcrn[index] + 1;
//                System.out.print(vn + " ");
                CGNS.intArray_setitem(vtxList, count, vn);
                count++;
            }
//            System.out.println();
        }
        _ierror = CGNS.cg_section_write(c, b, iz, "fluid", ElementType_t.MIXED,
                nele_start, nele_end, nbdyelement, vtxList, cell_section_index);
        checkError() ;
        
        
        // write boundary elements section
        int[] m2nc = d.getM2NC(); //offset in nface
        int[] m2nx = d.getM2NX(); //Number of faces on each element.
        int[] nface = d.getNFACE(); //Element to face connectivity
        
        if(d.getL2VT() == null){
            d.createFace2VertexMapping();
        }
        
        int[] l2vt = d.getL2VT(); //vertex connectivity for faces
        int[] l2cc = d.getL2CC(); // offset into vertex connectivity.
        int[] l2cx = d.getL2CX(); //No of vertex for each element.
        
        final int nReg = d.getNumberOfRegions();

        for (int r = 0; r < nReg; r++) {
            Region reg = d.getRegion(r);
            if (reg.isTypePair()) {
                intVector listOfVrtx = new intVector();
                
                int[] cells = reg.getCells();
                int[] sides = reg.getSides();
//                System.out.println("Total faces : " + sides.length);
                nele_start = nele_end + 1;
                nele_end = nele_start + cells.length - 1;
                nbdyelement = 0;
                for (int cell = 0; cell < cells.length; cell++) {
                    final int cellNo = cells[cell];
                    final int sideNo = sides[cell];
                    int nfaceOff = m2nc[cellNo] + sideNo;
                    int faceNo = nface[nfaceOff];
//                    System.out.println("cell no. : " + (cellNo + 1) + " side no. : " + (sideNo + 1) + " face no : " + faceNo);
                   
                    int nvrtxOnFace = l2cx[faceNo];
                    int l2vtOff = l2cc[faceNo];
                    
                    listOfVrtx.append(getBoundaryFaceType(nvrtxOnFace));
                    
                    for (int v = 0; v < nvrtxOnFace; v++) {
                        int index = l2vtOff + v;
                        int vn = l2vt[index] + 1;
                        listOfVrtx.append(vn);
//                        System.out.print(vn + " ");
                    }
//                    System.out.println();
                }

                SWIGTYPE_p_int cg_reg_l2vt = CGNS.new_intArray(listOfVrtx.size());
                for (int i = 0; i < listOfVrtx.size(); i++) {
//                    System.out.print(listOfVrtx.get(i) + " ");
                    CGNS.intArray_setitem(cg_reg_l2vt, i, listOfVrtx.get(i));
                }
//                System.out.println();
                _ierror = CGNS.cg_section_write(c, b, iz, reg.getName(), ElementType_t.MIXED,
                        nele_start, nele_end, nbdyelement, cg_reg_l2vt, cell_section_index);
                checkError() ;
                listOfVrtx = null;
            }

        }

        // write subzones for LOCAte PAIR


        // write subzones for LOCAte LIST


    } // end of method writeGrid
    
    private int getCGNSCellType(int acrCellType, int nNodes){
        ElementType_t type = null; 
        int intVal = -1;
        if(acrCellType == 0){
            //Triangle
            type = ElementType_t.TRI_3;
            intVal = type.swigValue();
        }else if(acrCellType == 1){
            //quad
            type = ElementType_t.QUAD_4;
            intVal = type.swigValue();
        }else if(acrCellType == 2){
            //tetrahedron
            type = ElementType_t.TETRA_4;
            intVal = type.swigValue();
        }else if(acrCellType == 3){
            //Pyramid
            type = ElementType_t.PYRA_5;
            intVal = type.swigValue();
        }else if(acrCellType == 4){
            //Prism
            type = ElementType_t.PENTA_6;
            intVal = type.swigValue();
        }else if(acrCellType == 5){
            //Hexahedron
            type = ElementType_t.HEXA_8;
            intVal = type.swigValue();
        }else {  //acrCellType == 6,7,8,9, >1000)
            type = ElementType_t.NGON_n;
            intVal = type.swigValue() + nNodes;
        }      
        return intVal;        
    }//end of getCGNSCellType
    
    private int getBoundaryFaceType(int numberOfVertex) {
        int acrCellType = -1;
        if (numberOfVertex == 2) {
            ElementType_t type = ElementType_t.BAR_2;
            return type.swigValue();
        } else if (numberOfVertex == 3) {
            acrCellType = 0;
        } else if (numberOfVertex == 4) {
            acrCellType = 1;
        } else if (numberOfVertex > 5) {
            acrCellType = 6;
        }
        return getCGNSCellType(acrCellType, numberOfVertex);
    }//End of getBoundaryFaceType

    public static void write( String folder, String fileName, DataSet d ) throws IOException {

    } // end of static method write
    
    
    public static void main(String[] args) throws IOException, AcrException {
        String cwd = System.getProperty("user.dir");
//        String cgns_file = "3d_unstru\\lid_unstr_small.cgns";

        String xyz = null; //"3d_unstru\\lid_unstr_small.xyz";
        String hyb = null; //"3d_unstru\\lid_unstr_small.hyb";
        String loc = null; //"3d_unstru\\lid_unstr_small.inp";
        int dim = -1;
        
        if(args.length >= 3){
            if(args[0] == "structure"){
                dim = 0;
            }else {
                dim = 3;
            }
            xyz = args[1];
            hyb = args[2];
            loc = args[3];
        }else {
            System.out.println("Error : Make sure you have entered all the argument "
                    + "requred to calculate in proper order");           
        }
        System.out.println();
        System.out.println("Mesh Type : " + args[0]);
        System.out.println("xyz/grd File : " + xyz);
        System.out.println("hyb File : " + hyb);
        System.out.println("loc/inp File : " + loc);
        System.out.println();
        
        DataSet d = DatasetLoadUtilities.createDataSet2(xyz, hyb, null, loc, 3, dim);
        AcrTocgns acr2cgns = new AcrTocgns();
        String fileName = "";
        if(xyz.contains(File.separator)){
            int start = xyz.lastIndexOf(File.separator);
            int end = xyz.lastIndexOf(".");
            String absolutePath = xyz.substring(0, start);
            fileName = absolutePath + xyz.substring(start, end) + ".cgns";
        }else {
            fileName = xyz.substring(0, xyz.indexOf(".")) + ".cgns";
        }
        
        System.out.println("CGNS File : " + fileName);

        acr2cgns.setFileName(fileName);
        acr2cgns.cg_open_for_write(d);
        acr2cgns.writeGrid(d);
        acr2cgns.cg_close();

    } // end of method main.
    
} // end of class TestCGNS01

