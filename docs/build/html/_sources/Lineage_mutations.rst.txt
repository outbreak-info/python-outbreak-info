lineage_mutations(pango_lin, mutation, freq)
--------------------------------------------

.. autofunction:: outbreak_data.lineage_mutations
 
Example usage:

1. Get a list of all mutations and relevant data associated with the variant 'B.1.1.7'::
    
    df = outbreak_data.lineage_mutations('b.1.1.7')
    print(df)

.. code-block::
   :caption: Output:
   
                  mutation  mutation_count  lineage_count  lineage   gene  \
    0                n:d3l         1133368        1154337  b.1.1.7      N   
    1              n:r203k         1131899        1154337  b.1.1.7      N   
    2              s:d614g         1150796        1154337  b.1.1.7      S   
    3         orf1a:t1001i         1149579        1154337  b.1.1.7  ORF1a   
    4            orf8:s84l         1148665        1154337  b.1.1.7   ORF8   
    5              s:a570d         1147678        1154337  b.1.1.7      S   
    6              s:p681h         1147591        1154337  b.1.1.7      S   
    7          orf1b:p314l         1147331        1154337  b.1.1.7  ORF1b   
    8             s:d1118h         1147009        1154337  b.1.1.7      S   
    9         orf1a:a1708d         1146288        1154337  b.1.1.7  ORF1a   
    10           orf8:y73c         1144041        1154337  b.1.1.7   ORF8   
    11             s:s982a         1142512        1154337  b.1.1.7      S   
    12           orf8:q27*         1142465        1154337  b.1.1.7   ORF8   
    13             s:t716i         1142087        1154337  b.1.1.7      S   
    14             n:s235f         1141424        1154337  b.1.1.7      N   
    15           orf8:r52i         1138388        1154337  b.1.1.7   ORF8   
    16             s:n501y         1129018        1154337  b.1.1.7      S   
    17        orf1a:i2230t         1127643        1154337  b.1.1.7  ORF1a   
    18  orf1a:del3675/3677         1115708        1154337  b.1.1.7  ORF1a   
    19          s:del69/70         1114288        1154337  b.1.1.7      S   
    20        s:del144/144         1093432        1154337  b.1.1.7      S   
    21             n:g204r         1050444        1154337  b.1.1.7      N   

                    ref_aa        alt_aa  codon_num codon_end          type  \
    0                    D             L          3      None  substitution   
    1                    R             K        203      None  substitution   
    2                    D             G        614      None  substitution   
    3                    T             I       1001      None  substitution   
    4                    S             L         84      None  substitution   
    5                    A             D        570      None  substitution   
    6                    P             H        681      None  substitution   
    7                    P             L        314      None  substitution   
    8                    D             H       1118      None  substitution   
    9                    A             D       1708      None  substitution   
    10                   Y             C         73      None  substitution   
    11                   S             A        982      None  substitution   
    12                   Q             *         27      None  substitution   
    13                   T             I        716      None  substitution   
    14                   S             F        235      None  substitution   
    15                   R             I         52      None  substitution   
    16                   N             Y        501      None  substitution   
    17                   I             T       2230      None  substitution   
    18  ORF1A:DEL3675/3677  DEL3675/3677       3675    3677.0      deletion   
    19          S:DEL69/70      DEL69/70         69      70.0      deletion   
    20        S:DEL144/144    DEL144/144        144     144.0      deletion   
    21                   G             R        204      None  substitution   

        prevalence change_length_nt  
    0     0.981835             None  
    1     0.980562             None  
    2     0.996932             None  
    3     0.995878             None  
    4     0.995086             None  
    5     0.994231             None  
    6     0.994156             None  
    7     0.993931             None  
    8     0.993652             None  
    9     0.993027             None  
    10    0.991081             None  
    11    0.989756             None  
    12    0.989715             None  
    13    0.989388             None  
    14    0.988813             None  
    15    0.986183             None  
    16    0.978066             None  
    17    0.976875             None  
    18    0.966536              9.0  
    19    0.965306              6.0  
    20    0.947238              3.0  
    21    0.909998             None  

2. Mutiple queries for lineages and mutations can be separated by ","::
    
    #Find mutation information for B.1.1.7, P.1, and XBB.1.5
    df = outbreak_data_lineage_mutations('b.1.1.7, p.1, xbb.1.5')
    print(df)

.. code-block::
   :caption: Output

            mutation  mutation_count  lineage_count  lineage   gene        ref_aa  \
    0          n:d3l         1133368        1154337  b.1.1.7      N             D   
    1        n:r203k         1131899        1154337  b.1.1.7      N             R   
    2        s:d614g         1150796        1154337  b.1.1.7      S             D   
    3   orf1a:t1001i         1149579        1154337  b.1.1.7  ORF1a             T   
    4      orf8:s84l         1148665        1154337  b.1.1.7   ORF8             S   
    ..           ...             ...            ...      ...    ...           ...   
    63       s:g446s          156244         167128  xbb.1.5      S             G   
    64  s:del144/144          154766         167128  xbb.1.5      S  S:DEL144/144   
    65       s:h146q          153308         167128  xbb.1.5      S             H   
    66       s:r408s          152365         167128  xbb.1.5      S             R   
    67       s:k417n          147604         167128  xbb.1.5      S             K   

            alt_aa  codon_num codon_end          type  prevalence change_length_nt  
    0            L          3      None  substitution    0.981835             None  
    1            K        203      None  substitution    0.980562             None  
    2            G        614      None  substitution    0.996932             None  
    3            I       1001      None  substitution    0.995878             None  
    4            L         84      None  substitution    0.995086             None  
    ..         ...        ...       ...           ...         ...              ...  
    63           S        446      None  substitution    0.934876             None  
    64  DEL144/144        144     144.0      deletion    0.926033              3.0  
    65           Q        146      None  substitution    0.917309             None  
    66           S        408      None  substitution    0.911667             None  
    67           N        417      None  substitution    0.883179             None  

[113 rows x 12 columns]

3. Use 'OR' in a string to return overlapping mutations in multiple lineages::

    df = outbreak_data.lineage_mutations('ba.2 OR xbb.1.5')
    print(df)

.. code-block::
   :caption: Output

                 mutation  mutation_count  lineage_count         lineage   gene  \
    0             n:r203k          237984         243206  P.1 OR xbb.1.5      N   
    1             s:d614g          242522         243206  P.1 OR xbb.1.5      S   
    2         orf1b:p314l          242226         243206  P.1 OR xbb.1.5  ORF1b   
    3             s:h655y          241765         243206  P.1 OR xbb.1.5      S   
    4           orf8:s84l          240116         243206  P.1 OR xbb.1.5   ORF8   
    5             n:g204r          238101         243206  P.1 OR xbb.1.5      N   
    6             s:n501y          235654         243206  P.1 OR xbb.1.5      S   
    7  orf1a:del3675/3677          226006         243206  P.1 OR xbb.1.5  ORF1a   

                   ref_aa        alt_aa  codon_num codon_end          type  \
    0                   R             K        203      None  substitution   
    1                   D             G        614      None  substitution   
    2                   P             L        314      None  substitution   
    3                   H             Y        655      None  substitution   
    4                   S             L         84      None  substitution   
    5                   G             R        204      None  substitution   
    6                   N             Y        501      None  substitution   
    7  ORF1A:DEL3675/3677  DEL3675/3677       3675    3677.0      deletion   

       prevalence change_length_nt  
    0    0.978528             None  
    1    0.997188             None  
    2    0.995970             None  
    3    0.994075             None  
    4    0.987295             None  
    5    0.979010             None  
    6    0.968948             None  
    7    0.929278              9.0 

 
