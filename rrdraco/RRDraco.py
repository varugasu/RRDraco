from rrdraco.rrdtool_wrapper import rrdtool
import re


class RRDraco(object):
    def __init__(self, rrd_file):
        self._info = rrdtool.info(rrd_file)
        self.ds = []
        self.rra = []
        self.version = None
        self.step = None
        self.schema = self._buildSchema(self._info)

    def _buildSchema(self, info):

        for line in info.splitlines():
            var, value = line.split('=')
            if re.match('rrd_version', var):
                self.version = value.strip().strip('"')
            if re.match('step', var):
                self.step = int(value)
            if re.match('ds', var):
                ds, attr = var.split('.')
                obj = self.get_ds(ds.partition('[')[-1].partition(']')[0])
                attr = attr.strip()
                value = value.strip()
                if attr == 'index':
                    obj.index = int(value)
                if attr == 'minimal_heartbeat':
                    obj.heartbeat = int(value)
                if attr == 'type':
                    obj.ds_type = value
                if attr == 'min':
                    obj.min_value = float(value)
                if attr == 'max':
                    obj.max_value = float(value)
            if re.match('rra', var):
                rra, attr = var.split('.', maxsplit=1)
                obj = self._get_rra(rra[4])
                attr = attr.strip()
                value = value.strip()
                if attr == 'cf':
                    obj.cf = value
                if attr == 'rows':
                    obj.rows = value
                if attr == 'xff':
                    obj.xff = value
                if attr == 'pdp_per_row':
                    obj.pdp_per_row = value

        schema = {
            "version": self.version,
            "step": self.step,
            "ds": [],
            "rra": []
        }

        for ds in self.ds:
            hold = {"name": ds.variable_name, "type": ds.ds_type,
                    "minimal_heartbeat": ds.heartbeat, "min": ds.min_value, "max": ds.max_value
                    }
            schema["ds"].append(hold)
        for rra in self.rra:
            hold = {"cf": rra.cf, "pdp_per_row": rra.pdp_per_row,
                    "xff": rra.xff, "rows": rra.rows}
            schema["rra"].append(hold)

        return schema

    def _get_rra(self, index):
        for rra in self.rra:
            if rra.index == index:
                return rra
        rra = RRA(index)
        self.rra.append(rra)
        return rra

    def get_ds(self, variable_name):
        for ds in self.ds:
            if variable_name == ds.variable_name:
                return ds
        ds = DS(variable_name)
        self.ds.append(ds)
        return ds


class RRA(object):
    def __init__(self, index, cf=None, xff=None, pdp_per_row=None, rows=None):
        self.index = index
        self.cf = cf
        self.xff = xff
        self.pdp_per_row = pdp_per_row
        self.rows = rows


class DS(object):
    def __init__(self, variable_name, index=None, ds_type=None, heartbeat=None, min_value=None, max_value=None):
        self.variable_name = variable_name
        self.index = index
        self.ds_type = ds_type
        self.heartbeat = heartbeat
        self.min_value = min_value

    def __str__(self):
        return self.variable_name
