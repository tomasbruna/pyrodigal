import gzip
import os
import unittest

import Bio.SeqIO
from pyrodigal import Pyrodigal



class TestPyrodigalMeta(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        data = os.path.realpath(os.path.join(__file__, "..", "data"))
        fna = os.path.join(data, "SRR492066.fna.gz")
        meta_fna = os.path.join(data, "SRR492066.meta.fna.gz")
        meta_faa = os.path.join(data, "SRR492066.meta.faa.gz")

        with gzip.open(fna, "rt") as f:
            cls.record = next(Bio.SeqIO.parse(f, "fasta"))
        with gzip.open(meta_faa, "rt") as f:
            cls.proteins = [
                record
                for record in Bio.SeqIO.parse(f, "fasta")
                if record.id.startswith("{}_".format(cls.record.id))
            ]
        with gzip.open(meta_fna, "rt") as f:
            cls.genes = [
                record
                for record in Bio.SeqIO.parse(f, "fasta")
                if record.id.startswith("{}_".format(cls.record.id))
            ]

        cls.p = Pyrodigal(meta=True)
        cls.preds = cls.p.find_genes(str(cls.record.seq))

    def test_translate(self):
        self.assertEqual(len(self.preds), len(self.proteins))
        for gene, protein in zip(self.preds, self.proteins):
            self.assertEqual(gene.translate(), str(protein.seq))

    def test_coordinates(self):
        self.assertEqual(len(self.preds), len(self.proteins))
        for gene, protein in zip(self.preds, self.proteins):
            id_, start, end, strand, *_ = protein.description.split(" # ")
            self.assertEqual(gene.begin, int(start))
            self.assertEqual(gene.end, int(end))
            self.assertEqual(gene.strand, int(strand))

    def test_rbs_motif(self):
        self.assertEqual(len(self.preds), len(self.proteins))
        for gene, protein in zip(self.preds, self.proteins):
            *_, raw_data = protein.description.split(" # ")
            data = dict(keyval.split("=") for keyval in raw_data.split(";"))
            if data["rbs_motif"] != "None":
                self.assertEqual(gene.rbs_motif, data["rbs_motif"])
            else:
                self.assertIs(gene.rbs_motif, None)

    def test_rbs_spacer(self):
        self.assertEqual(len(self.preds), len(self.proteins))
        for gene, protein in zip(self.preds, self.proteins):
            *_, raw_data = protein.description.split(" # ")
            data = dict(keyval.split("=") for keyval in raw_data.split(";"))
            if data["rbs_spacer"] != "None":
                self.assertEqual(gene.rbs_spacer, data["rbs_spacer"])
            else:
                self.assertIs(gene.rbs_spacer, None)

    def test_start_type(self):
        self.assertEqual(len(self.preds), len(self.proteins))
        for gene, protein in zip(self.preds, self.proteins):
            *_, raw_data = protein.description.split(" # ")
            data = dict(keyval.split("=") for keyval in raw_data.split(";"))
            self.assertEqual(gene.start_type, data["start_type"])
