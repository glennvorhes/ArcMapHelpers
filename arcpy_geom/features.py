from .vertex import Vertex
import arcpy
from abc import abstractmethod, abstractproperty
from datetime import datetime


def _prepare_db_values(v_dict, date_format='%Y-%m-%d'):
    """

    :param v_dict:
    :type v_dict: dict
    :param date_format:
    :type date_format:
    :return:
    :rtype:
    """
    return_dict = {}

    for k, v in v_dict.items():
        key = k.lower()
        return_dict[key] = v

        if return_dict[key] is None:
            return_dict[key] = 'NULL'
        elif isinstance(return_dict[key], str):
            return_dict[key] = "'{0}'".format(return_dict[key])
        elif isinstance(return_dict[key], datetime):
            return_dict[key] = "date '{0}'".format(return_dict[key].strftime(date_format))
        else:
            try:
                return_dict[key] = float(return_dict[key])

                if return_dict[key] % 1 == 0:
                    return_dict[key] = int(return_dict[key])

                return_dict[key] = str(return_dict[key])
            except ValueError as ex:
                if isinstance(return_dict[key], unicode):
                    return_dict[key] = "'{0}'".format(return_dict[key].encode('utf-8').replace("'", r"\'"))
                else:
                    print(type(return_dict[key]))
                    print(return_dict[key])
                    raise ex

    return return_dict


class Feature:
    def __init__(self, vertices, props=None, multipart=False):
        # self._vertices = coords

        self._vertices = vertices
        # """
        # :type: list[Vertex]||list[list[Vertex]]||list[list[list[Vertex]]]
        # """

        self.properties = props or {}
        self._shape = None
        self._multipart = multipart
        self._build_geom()

    @property
    def shape(self):
        self._build_geom()

        if self._shape is None:
            raise NotImplementedError('shape has not been set')
        return self._shape

    @property
    def multipart(self):
        return self._multipart

    def get_property(self, prop):
        if prop in self.properties.keys():
            return self.properties[prop]
        else:
            return None

    def set_property(self, prop, val):
        self.properties[prop] = val

    # @property
    # def coords(self):
    #     return self._vertices

    @property
    def vertices(self):
        """

        # :return:
        # :rtype: list[Vertex]
        # """
        return self._vertices

    @abstractmethod
    def _build_geom(self):
        pass

    def as_postgres_sql(self, table_name, srid, include_columns=None, fixed_values=None, geom_column='geom', date_format='%Y-%m-%d'):
        fixed_values = fixed_values or {}
        include_columns = include_columns or []

        p = _prepare_db_values(fixed_values, date_format)

        f_props = _prepare_db_values(self.properties, date_format)

        if len(include_columns) > 0:
            f_props = {k: v for k, v in f_props.items() if k in include_columns}

        for k, v in f_props.items():
            p[k] = v

        p[geom_column] = "ST_GeomFromText('{geom}', {srid})".format(geom=self.wkt, srid=srid)

        cols = []
        vals = []

        for k, v in p.items():
            cols.append(k)
            vals.append(v)

        return 'INSERT INTO {table} ({cols}) VALUES ({vals});'.format(
            table=table_name,
            cols=', '.join(cols),
            vals=', '.join(vals)
        )

    @property
    def wkt(self):
        raise NotImplementedError

    @abstractproperty
    def geom_type(self):
        pass


class Point(Feature):
    def __init__(self, vertices, props=None):
        """

        :param vertices:
        :type vertices: list[Vertex]
        :param props:
        :type props:
        """

        Feature.__init__(self, vertices, props)

    def _build_geom(self):
        v = self.vertices[0]
        self._shape = arcpy.Point(**v.kw)

    @property
    def wkt(self):

        if self.multipart:
            raise NotImplementedError
        else:
            v = self.vertices[0]
            ret = 'POINT ({x} {y})'.format(x=v.x, y=v.y)
            return ret

    @property
    def geom_type(self):
        return 'point'


class MultiPoint(Feature):
    def __init__(self, vertices, props=None):
        vertices = vertices[0]
        Feature.__init__(self, vertices, props)

    def _build_geom(self):
        arr = []
        for v in self._vertices:
            arr.append(arcpy.Point(**v.kw))

        self._shape = arcpy.Multipoint(arcpy.Array(arr))

    @property
    def geom_type(self):
        return 'multipoint'


class LineString(Feature):
    def __init__(self, vertices, props=None):

        multi = False

        if len(vertices) == 0:
            vertices = []
        elif isinstance(vertices[0], Vertex):
            pass
        elif isinstance(vertices[0], list) and len(vertices) == 1:
            vertices = vertices[0]
        else:
            multi = True

        Feature.__init__(self, vertices, props, multipart=multi)

    def add_m(self):
        if self.multipart:
            for i in range(len(self._vertices)):
                cumul_len = 0
                for j in range(len(self.vertices[i])):
                    if j > 0:
                        cumul_len += self._vertices[i][j].get_2d_dist(self._vertices[i][j - 1])
                    self._vertices[i][j].m = cumul_len
        else:
            cumul_len = 0
            for i in range(len(self._vertices)):
                if i > 0:
                    cumul_len += self._vertices[i].get_2d_dist(self._vertices[i - 1])
                self._vertices[i].m = cumul_len

        self._build_geom()

    def _build_geom(self):

        if len(self._vertices) == 0:
            return

        arcpy_vert_list = []

        if self.multipart:
            for i in range(len(self._vertices)):
                ll = self._vertices[i]
                """
                :type: list[Vertex]
                """
                part = []
                for j in range(len(ll)):
                    v = ll[j]
                    part.append(arcpy.Point(**v.kw))
                    arcpy_vert_list.append(arcpy.Array(part))
        else:
            for i in range(len(self._vertices)):
                v = self._vertices[i]
                """
                :type: Vertex
                """
                arcpy_vert_list.append(arcpy.Point(**v.kw))

        self._shape = arcpy.Polyline(arcpy.Array(arcpy_vert_list))

    def add_vertex(self, v):
        """

        :param v:
        :type v: Vertex
        """
        assert isinstance(v, Vertex)
        if len(self._vertices) > 0 and not isinstance(self._vertices[0], Vertex):
            raise ValueError('base list is not vertex, is multipart')
        self._vertices.append(v)
        self._vertices.append(v.as_list())

    def extend_vertices(self, v_list):
        """

        :param v_list:
        :type v_list: list[Vertex]
        :return:
        :rtype:
        """
        if len(self._vertices) > 0 and not isinstance(self._vertices[0], Vertex):
            raise ValueError('base list is not vertex, is multipart')
        self._vertices.extend(v_list)

        # for v in v_list:
        #     self._coords.append(v.as_list())

    @property
    def num_vertices(self):
        if len(self._vertices) == 0:
            return 0
        elif isinstance(self._vertices[0], Vertex):
            return len(self._vertices)
        else:
            num_verts = 0

            for l in self._vertices:
                num_verts += len(l)
            return num_verts

    @property
    def wkt(self):

        if self.multipart:
            raise NotImplementedError
        else:
            ret = 'LINESTRING ({0})'.format(', '.join([v.as_wkt for v in self.vertices]))
            return ret

    @property
    def geom_type(self):
        return 'linestring'

    def flip_vertices(self):
        if self.multipart:
            for v_list in self.vertices:
                v_list.reverse()
        else:
            self.vertices.reverse()


class Polygon(Feature):
    def __init__(self, coords, props=None):
        Feature.__init__(self, coords, props)

    def _build_geom(self):
            vert_list = []

            if isinstance(self._vertices[0][0], Vertex):
                # single part
                for i in range(len(self._vertices)):
                    ring = []
                    for j in range(len(self._vertices[i])):
                        v = self._vertices[i][j]
                        """
                        :type: Vertex
                        """
                        ring.append(arcpy.Point(**v.kw))
                    vert_list.append(arcpy.Array(ring))
            else:
                self._multipart = True
                for i in range(len(self._vertices)):
                    part = []
                    for j in range(len(self._vertices[i])):
                        ring = []

                        for k in range(len(self._vertices[i][j])):
                            v = self._vertices[i][j][k]
                            """
                            :type: Vertex
                            """
                            ring.append(arcpy.Point(**v.kw))

                        part.append(arcpy.Array(ring))
                    vert_list.append(arcpy.Array(part))

            self._shape = arcpy.Polygon(arcpy.Array(vert_list))

    @property
    def geom_type(self):
        return 'polygon'
