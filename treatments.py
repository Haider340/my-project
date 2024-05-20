import json

class Treatment:
    def __init__(self, name, description, category):
        self.name = name
        self.description = description
        self.category = category

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'category': self.category
        }

class Disease:
    def __init__(self, name, treatments):
        self.name = name
        self.treatments = [Treatment(**t) for t in treatments]

    def to_dict(self):
        return {
            'name': self.name,
            'treatments': [t.to_dict() for t in self.treatments]
        }

class TreatmentManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.diseases = self.load_diseases()

    def load_diseases(self):
        try:
            with open(self.filepath, 'r') as file:
                data = json.load(file)
                return [Disease(**d) for d in data.get('diseases', [])]
        except FileNotFoundError:
            return []

    def save_diseases(self):
        with open(self.filepath, 'w') as file:
            json.dump({'diseases': [d.to_dict() for d in self.diseases]}, file, indent=4)

    def list_diseases(self):
        return self.diseases

    def find_disease(self, name):
        for disease in self.diseases:
            if disease.name.lower() == name.lower():
                return disease
        return None
