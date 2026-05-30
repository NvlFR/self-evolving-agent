import numpy as np

class Guard:
    def __init__(self, optimal_threshold: float = 1.0):
        self.optimal_threshold = optimal_threshold
        self.is_optimal = False

    def is_allowed_mutation(self, current_score: float) -> bool:
        """Mengecek apakah mutasi dapat dilakukan berdasarkan skor performa.

        Args:
            current_score (float): Skor performa model pada iterasi terkini.

        Returns:
            bool: True jika mutasi diizinkan, False jika blokir.
        """
        if current_score >= self.optimal_threshold:
            self.is_optimal = True
            return False  # blokir mutasi
        self.is_optimal = False
        return True   # izinkan mutasi

    def should_preserve(self, score: float) -> bool:
        """Alias untuk kompatibilitas dengan logika sebelumnya.

        Args:
            score (float): Skor performa.

        Returns:
            bool: True jika performa sudah optimal, artinya simpan.
        """
        return score >= self.optimal_threshold