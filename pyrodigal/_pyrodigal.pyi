import threading
import typing
from typing import Iterable, Iterator, Optional, Set, TextIO, Tuple, Union

# --- Globals ----------------------------------------------------------------

_TRANSLATION_TABLES: Set[int]
METAGENOMIC_BINS: Tuple[MetagenomicBin]


# --- Sequence mask ----------------------------------------------------------

class Mask:
    @property
    def begin(self) -> int: ...
    @property
    def end(self) -> int: ...

class Masks(typing.Sequence[Mask]):
    def __sizeof__(self) -> int: ...
    def __len__(self) -> int: ...
    def __getitem__(self, index: int) -> Mask: ...
    def __iter__(self) -> Iterator[Mask]: ...
    def __reversed__(self) -> Iterator[Mask]: ...
    def clear(self) -> None: ...
    def copy(self) -> Masks: ...

# --- Input sequence ---------------------------------------------------------

class Sequence(typing.Sized):
    gc: float
    @classmethod
    def from_bytes(cls, sequence: Union[bytes, bytearray]) -> Sequence: ...
    @classmethod
    def from_string(cls, sequence: str) -> Sequence: ...
    def __len__(self) -> int: ...

# --- Nodes ------------------------------------------------------------------

class Node:
    owner: Nodes
    @property
    def type(self) -> str: ...
    @property
    def edge(self) -> bool: ...
    @property
    def gc_bias(self) -> int: ...
    @property
    def cscore(self) -> float: ...
    @property
    def gc_cont(self) -> float: ...
    @property
    def score(self) -> float: ...

class Nodes(typing.Sequence[Node]):
    def __copy__(self) -> Nodes: ...
    def __sizeof__(self) -> int: ...
    def __len__(self) -> int: ...
    def __getitem__(self, index: int) -> Node: ...
    def __iter__(self) -> Iterator[Node]: ...
    def __reversed__(self) -> Iterator[Node]: ...
    def clear(self) -> None: ...
    def copy(self) -> Nodes: ...
    def sort(self) -> None: ...

# --- Genes ------------------------------------------------------------------

class Gene:
    @property
    def begin(self) -> int: ...
    @property
    def end(self) -> int: ...
    @property
    def start_ndx(self) -> int: ...
    @property
    def stop_ndx(self) -> int: ...

class Genes(typing.Sequence[Gene]):
    def __len__(self) -> int: ...
    def __getitem__(self, index: int) -> Gene: ...
    def __iter__(self) -> Iterator[Gene]: ...
    def __reversed__(self) -> Iterator[Gene]: ...
    def clear(self) -> None: ...

# --- Training Info ----------------------------------------------------------

class TrainingInfo:
    @property
    def translation_table(self) -> int: ...
    @translation_table.setter
    def translation_table(self, table: int) -> None: ...
    @property
    def gc(self) -> float: ...
    @gc.setter
    def gc(self, gc: float) -> None: ...
    @property
    def bias(self) -> Tuple[float, float, float]: ...
    @bias.setter
    def bias(self, bias: Iterable[float]) -> None: ...
    @property
    def type_weights(self) -> Tuple[float, float, float]: ...
    @type_weights.setter
    def type_weights(self, type_weights: Iterable[float]) -> None: ...
    @property
    def uses_sd(self) -> bool: ...
    @uses_sd.setter
    def uses_sd(self, uses_sd: bool) -> None: ...
    @property
    def start_weight(self) -> float: ...
    @start_weight.setter
    def start_weight(self, st_wt: float) -> None: ...

# --- Metagenomic Bins -------------------------------------------------------

class MetagenomicBin:
    training_info: TrainingInfo
    @property
    def index(self) -> int: ...
    @property
    def description(self) -> str: ...

# --- Predictions ------------------------------------------------------------

class Prediction:
    owner: Predictions
    gene: Gene

    @property
    def _gene_data(self) -> str: ...
    @property
    def _score_data(self) -> str: ...
    @property
    def begin(self) -> int: ...
    @property
    def end(self) -> int: ...
    @property
    def strand(self) -> int: ...
    @property
    def partial_begin(self) -> bool: ...
    @property
    def partial_end(self) -> bool: ...
    @property
    def start_type(self) -> str: ...
    @property
    def rbs_motif(self) -> Optional[str]: ...
    @property
    def rbs_spacer(self) -> Optional[str]: ...
    @property
    def gc_cont(self) -> float: ...
    @property
    def translation_table(self) -> int: ...
    @property
    def cscore(self) -> float: ...
    @property
    def rscore(self) -> float: ...
    @property
    def sscore(self) -> float: ...
    @property
    def tscore(self) -> float: ...
    @property
    def uscore(self) -> float: ...
    def confidence(self) -> float: ...
    def translate(self, translation_table: Optional[int] = None, unknown_residue: str = "X") -> str: ...

class Predictions(typing.Sequence[Prediction]):
    def __bool__(self) -> int: ...
    def __len__(self) -> int: ...
    def __getitem__(self, index: int) -> Prediction: ...
    def __iter__(self) -> Iterator[Prediction]: ...
    def __reversed__(self) -> Iterator[Prediction]: ...
    def write_gff(self, file: TextIO, prefix: str = "gene_", tool: str = "pyrodigal") -> int: ...
    def write_genes(self, file: TextIO, prefix: str ="gene_", width: typing.Optional[int] = 70) -> int: ...
    def write_translations(self, file: TextIO, prefix: str = "gene_", width: typing.Optional[int] = 60, translation_table: typing.Optional[int] = None) -> int: ...

# --- Pyrodigal --------------------------------------------------------------

class OrfFinder:
    closed: bool
    meta: bool
    lock: threading.Lock
    _num_seq: int

    def __init__(self, meta: bool = False, closed: bool = False) -> None: ...
    def __repr__(self) -> str: ...
    def find_genes(self, sequence: Union[str, bytes, bytearray]) -> Predictions: ...
    def train(
        self,
        sequence: str,
        force_nonsd: bool = False,
        st_wt: float = 4.35,
        translation_table: int = 11,
    ) -> TrainingInfo: ...
