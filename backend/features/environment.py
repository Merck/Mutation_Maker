#    Copyright (c) 2020 Merck Sharp & Dohme Corp. a subsidiary of Merck & Co., Inc., Kenilworth, NJ, USA.
#
#    This file is part of the Mutation Maker, An Open Source Oligo Design Software For Mutagenesis and De Novo Gene Synthesis Experiments.
#
#    Mutation Maker is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from behave import register_type
from parse_type import TypeBuilder
from Bio.Seq import Seq

parse_primer_direction = TypeBuilder.make_choice(["forward", "reverse"])
register_type(PrimerDirection=parse_primer_direction)


def parse_sequence(sequence):
    if type(sequence) == Seq:
        return sequence
    seq = Seq(sequence)
    return seq.ungap(" ")


register_type(Sequence=parse_sequence)
