import json
from brain.llm_client import llm
from memory.status_manager import status_manager

class MutationEngine:
    def __init__(self):
        pass

    def generate_repair_mutation(self, issue: dict):
        prompt = f"""
        Kamu adalah Mesin Perbaikan (Repair Engine) Sistem Evolusi SEED. 
        Tugasmu adalah memperbaiki masalah yang dilaporkan di dalam kode.

        Masalah yang Dilaporkan:
        Judul: {issue['title']}
        Deskripsi: {issue['body']}

        Berikan usulan perbaikan kode spesifik. 
        Kembalikan usulanmu dalam objek JSON dengan:
        {{
            "type": "modify_file",
            "file_path": "path/ke/file.py",
            "description": "Perbaikan untuk issue: {issue['title']}",
            "code": "Kode lengkap yang sudah diperbaiki untuk file tersebut",
            "instruction": "Langkah-langkah menerapkan perbaikan"
        }}
        CATATAN: Deskripsi dan Instruksi HARUS dalam Bahasa Indonesia.
        """
        messages = [{"role": "user", "content": prompt}]
        response = llm.completion(messages, request_type="evolution")
        try:
            json_str = llm.extract_json(response)
            return json.loads(json_str)
        except: return None

    def generate_mutation(self, reflection: dict = None):
        current_context = status_manager.get_context()
        prompt = f"""
        Kamu adalah Mesin Mutasi Sistem Evolusi SEED. 
        {current_context}

        Tujuanmu adalah mengusulkan modifikasi kode, 'tool' baru, atau tindakan 'riset' 
        untuk meningkatkan performa atau kemampuan agen.

        AKSES DUNIA NYATA:
        Kamu memiliki akses ke 'RealWorldTool' yang bisa mencari di web dan GitHub.
        Jika kamu mengidentifikasi skill yang kurang, error yang asing, atau butuh algoritma kompleks, 
        kamu harus terlebih dahulu mengusulkan tindakan 'research' untuk belajar dari internet.

        Analisis/Refleksi Saat Ini:
        {json.dumps(reflection, indent=2) if reflection else "Tidak ada refleksi sebelumnya."}

        Usulkan perubahan:
        1. 'modify_file': Mengubah kode yang sudah ada di file.
        2. 'create_tool': Membuat file Python baru di folder 'brain/'.
        3. 'research': Mengusulkan query pencarian untuk mengumpulkan informasi dari web/GitHub.

        Kembalikan usulanmu dalam objek JSON dengan:
        {{
            "type": "modify_file" | "create_tool" | "research",
            "file_path": "path/ke/file.py (untuk kode)",
            "query": "query pencarian (untuk riset)",
            "description": "Penjelasan singkat dalam Bahasa Indonesia",
            "code": "Kode lengkap baru atau kode pengganti",
            "instruction": "Instruksi penerapan dalam Bahasa Indonesia"
        }}
        PENTING: Semua penjelasan (description, instruction) HARUS menggunakan Bahasa Indonesia.
        """
        
        messages = [{"role": "user", "content": prompt}]
        response = llm.completion(messages, request_type="evolution")
        
        if not response or response == "ERROR_QUOTA":
            return None
            
        try:
            json_str = llm.extract_json(response)
            if not json_str:
                return None
            mutation_data = json.loads(json_str)
            return mutation_data
        except Exception as e:
            print(f"Error parsing mutation proposal: {e}")
            return None
