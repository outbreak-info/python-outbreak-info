wildcard_lineage
------------------

.. autofunction:: outbreak_data.wildcard_lineage

**Example Usage**

List all known lineages that start with 'g'::

    >>> df = outbreak_data.wildcard_lineage('g*')
    >>> df

            total_count
    name               
    gk.1.1         5683
    gj.1.2         5610
    ge.1           4469
    gs.4.1         4368
    gk.1           1777
    ...             ...
    ga.7              1
    ga.7.2            1
    gd.3              1
    gl.2              1
    gy.2              1

    [156 rows x 1 columns]

Find lineages that contain '.86'::

    >>> df = outbreak_data.wildcard_lineage('*.86*')
    >>> df

                total_count
    name                   
    ba.2.86.1         10989
    b.1.177.86         5498
    ay.86              1105
    ba.2.86             995
    ba.2.86.3           366
    ba.2.86.2           323
    xbb.1.5.86          170
    ba.2.86.5            38
    b.1.1.86             26
    ba.2.86.4            10
