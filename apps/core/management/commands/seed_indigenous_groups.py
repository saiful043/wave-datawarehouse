from django.core.management.base import BaseCommand
from apps.core.models import IndigenousGroupType


class Command(BaseCommand):
    help = 'Clears table and seeds IndigenousGroupType data'

    def handle(self, *args, **kwargs):
        # ১. টেবিলের সব পুরানো ডাটা মুছে ফেলা (Truncate/Delete)
        deleted_count, _ = IndigenousGroupType.objects.all().delete()
        self.stdout.write(self.style.WARNING(f'Cleared {deleted_count} existing records from core_indigenous_group_type.'))

        raw_options = [
            {"value": "1", "labelEn": "Chakma", "labelBn": "চাকমা", "status": 1, "score": 0, "colorHex": None, "displayOrder": 11, "visibleWhen": None},
            {"value": "2", "labelEn": "Marma", "labelBn": "মারমা", "status": 1, "score": 0, "colorHex": None, "displayOrder": 34, "visibleWhen": None},
            {"value": "3", "labelEn": "Santal", "labelBn": "সাঁওতাল", "status": 1, "score": 0, "colorHex": None, "displayOrder": 46, "visibleWhen": None},
            {"value": "4", "labelEn": "Monipuri", "labelBn": "মনিপুরি", "status": 1, "score": 0, "colorHex": None, "displayOrder": 35, "visibleWhen": None},
            {"value": "5", "labelEn": "Garo", "labelBn": "গারো", "status": 1, "score": 0, "colorHex": None, "displayOrder": 13, "visibleWhen": None},
            {"value": "6", "labelEn": "Tripuri", "labelBn": "ত্রিপুরী", "status": 1, "score": 0, "colorHex": None, "displayOrder": 49, "visibleWhen": None},
            {"value": "7", "labelEn": "Rakhain", "labelBn": "রাখাইন", "status": 1, "score": 0, "colorHex": None, "displayOrder": 44, "visibleWhen": None},
            {"value": "8", "labelEn": "Khasia/Khasi", "labelBn": "খাসিয়া", "status": 1, "score": 0, "colorHex": None, "displayOrder": 22, "visibleWhen": None},
            {"value": "9", "labelEn": "Hajong", "labelBn": "হাজং", "status": 1, "score": 0, "colorHex": None, "displayOrder": 17, "visibleWhen": None},
            {"value": "10", "labelEn": "Koch", "labelBn": "কচ", "status": 1, "score": 0, "colorHex": None, "displayOrder": 25, "visibleWhen": None},
            {"value": "11", "labelEn": "Mro", "labelBn": "ম্রো", "status": 1, "score": 0, "colorHex": None, "displayOrder": 36, "visibleWhen": None},
            {"value": "12", "labelEn": "Tanchangya", "labelBn": "তঞ্চঙ্গ্য", "status": 1, "score": 0, "colorHex": None, "displayOrder": 47, "visibleWhen": None},
            {"value": "13", "labelEn": "Oraon", "labelBn": "ওঁরাও", "status": 1, "score": 0, "colorHex": None, "displayOrder": 39, "visibleWhen": None},
            {"value": "16", "labelEn": "Bom", "labelBn": "বম", "status": 1, "score": 0, "colorHex": None, "displayOrder": 8, "visibleWhen": None},
            {"value": "17", "labelEn": "Others (Specify)", "labelBn": "অন্যান্য (নির্দিষ্ট করুন)", "status": 1, "score": 0, "colorHex": None, "displayOrder": 51, "visibleWhen": None},
            {"value": "18", "labelEn": "Khumi", "labelBn": "খুমি", "status": 1, "score": 0, "colorHex": None, "displayOrder": 23, "visibleWhen": None},
            {"value": "19", "labelEn": "Khyang", "labelBn": "খিয়াং", "status": 1, "score": 0, "colorHex": None, "displayOrder": 24, "visibleWhen": None},
            {"value": "20", "labelEn": "Lusai", "labelBn": "লুসাই", "status": 1, "score": 0, "colorHex": None, "displayOrder": 31, "visibleWhen": None},
            {"value": "21", "labelEn": "Pankhoa/Pankho", "labelBn": "পাংখোয়া", "status": 1, "score": 0, "colorHex": None, "displayOrder": 41, "visibleWhen": None},
            {"value": "22", "labelEn": "Bagdi", "labelBn": "বাগদী", "status": 1, "score": 0, "colorHex": None, "displayOrder": 1, "visibleWhen": None},
            {"value": "23", "labelEn": "Banai", "labelBn": "বানাই", "status": 1, "score": 0, "colorHex": None, "displayOrder": 2, "visibleWhen": None},
            {"value": "24", "labelEn": "Barman", "labelBn": "বর্মন", "status": 1, "score": 0, "colorHex": None, "displayOrder": 3, "visibleWhen": None},
            {"value": "25", "labelEn": "Bedia", "labelBn": "বেদিয়া", "status": 1, "score": 0, "colorHex": None, "displayOrder": 4, "visibleWhen": None},
            {"value": "26", "labelEn": "Bhil", "labelBn": "ভীল", "status": 1, "score": 0, "colorHex": None, "displayOrder": 5, "visibleWhen": None},
            {"value": "27", "labelEn": "Bhuimali", "labelBn": "ভূইমালী", "status": 1, "score": 0, "colorHex": None, "displayOrder": 6, "visibleWhen": None},
            {"value": "28", "labelEn": "Bhumij", "labelBn": "ভূমিজ", "status": 1, "score": 0, "colorHex": None, "displayOrder": 7, "visibleWhen": None},
            {"value": "29", "labelEn": "Boraik/Baraik", "labelBn": "বড়াইক", "status": 1, "score": 0, "colorHex": None, "displayOrder": 9, "visibleWhen": None},
            {"value": "30", "labelEn": "Chak", "labelBn": "চাক", "status": 1, "score": 0, "colorHex": None, "displayOrder": 10, "visibleWhen": None},
            {"value": "31", "labelEn": "Dalu", "labelBn": "ডালু", "status": 1, "score": 0, "colorHex": None, "displayOrder": 12, "visibleWhen": None},
            {"value": "32", "labelEn": "Gonju", "labelBn": "গঞ্জু", "status": 1, "score": 0, "colorHex": None, "displayOrder": 14, "visibleWhen": None},
            {"value": "33", "labelEn": "Gorait", "labelBn": "গরাইত", "status": 1, "score": 0, "colorHex": None, "displayOrder": 15, "visibleWhen": None},
            {"value": "34", "labelEn": "Gurkha", "labelBn": "গোর্খা", "status": 1, "score": 0, "colorHex": None, "displayOrder": 16, "visibleWhen": None},
            {"value": "35", "labelEn": "Ho", "labelBn": "হো", "status": 1, "score": 0, "colorHex": None, "displayOrder": 18, "visibleWhen": None},
            {"value": "36", "labelEn": "Hudi", "labelBn": "হুদি", "status": 1, "score": 0, "colorHex": None, "displayOrder": 19, "visibleWhen": None},
            {"value": "37", "labelEn": "Kharia", "labelBn": "খাড়িয়া", "status": 1, "score": 0, "colorHex": None, "displayOrder": 20, "visibleWhen": None},
            {"value": "38", "labelEn": "Kharwar/Kherwar", "labelBn": "খারওয়ার", "status": 1, "score": 0, "colorHex": None, "displayOrder": 21, "visibleWhen": None},
            {"value": "39", "labelEn": "Kol", "labelBn": "কোল", "status": 1, "score": 0, "colorHex": None, "displayOrder": 26, "visibleWhen": None},
            {"value": "40", "labelEn": "Kondo", "labelBn": "কন্দ", "status": 1, "score": 0, "colorHex": None, "displayOrder": 27, "visibleWhen": None},
            {"value": "41", "labelEn": "Kora", "labelBn": "কোড়া", "status": 1, "score": 0, "colorHex": None, "displayOrder": 28, "visibleWhen": None},
            {"value": "42", "labelEn": "Lohar", "labelBn": "লোহার", "status": 1, "score": 0, "colorHex": None, "displayOrder": 30, "visibleWhen": None},
            {"value": "43", "labelEn": "Mahali", "labelBn": "মাহালী", "status": 1, "score": 0, "colorHex": None, "displayOrder": 32, "visibleWhen": None},
            {"value": "44", "labelEn": "Kurmi Mahato", "labelBn": "কুর্মি মাহাতো", "status": 1, "score": 0, "colorHex": None, "displayOrder": 29, "visibleWhen": None},
            {"value": "45", "labelEn": "Malo/Ghasimalo", "labelBn": "মালো/ঘাসিমালো", "status": 1, "score": 0, "colorHex": None, "displayOrder": 33, "visibleWhen": None},
            {"value": "46", "labelEn": "Munda", "labelBn": "মুন্ডা", "status": 1, "score": 0, "colorHex": None, "displayOrder": 37, "visibleWhen": None},
            {"value": "47", "labelEn": "Musahar", "labelBn": "মুসহর", "status": 1, "score": 0, "colorHex": None, "displayOrder": 38, "visibleWhen": None},
            {"value": "48", "labelEn": "Pahari/Mal Pahari", "labelBn": "পাহাড়ি/মাল পাহাড়ি", "status": 1, "score": 0, "colorHex": None, "displayOrder": 40, "visibleWhen": None},
            {"value": "49", "labelEn": "Patro", "labelBn": "পাত্র", "status": 1, "score": 0, "colorHex": None, "displayOrder": 42, "visibleWhen": None},
            {"value": "50", "labelEn": "Rajoar", "labelBn": "রাজোয়াড়", "status": 1, "score": 0, "colorHex": None, "displayOrder": 43, "visibleWhen": None},
            {"value": "51", "labelEn": "Sabar", "labelBn": "সাবার", "status": 1, "score": 0, "colorHex": None, "displayOrder": 45, "visibleWhen": None},
            {"value": "52", "labelEn": "Teli", "labelBn": "তেলী", "status": 1, "score": 0, "colorHex": None, "displayOrder": 48, "visibleWhen": None},
            {"value": "53", "labelEn": "Turi", "labelBn": "তুরি", "status": 1, "score": 0, "colorHex": None, "displayOrder": 50, "visibleWhen": None}
        ]

        # ২. displayOrder অনুযায়ী সাজানো
        sorted_options = sorted(raw_options, key=lambda item: item['displayOrder'])

        # ৩. Model Instances তৈরি
        objects_to_create = [
            IndigenousGroupType(
                id=int(item['value']),
                label_en=item['labelEn'],
                label_bn=item['labelBn'],
                status=item['status'],
                score=item['score'],
                color_hex=item['colorHex'],
                display_order=item['displayOrder'],
                visible_when=item['visibleWhen'],
            )
            for item in sorted_options
        ]

        # ৪. নতুনভাবে ডাটা ইনসার্ট
        IndigenousGroupType.objects.bulk_create(objects_to_create)

        self.stdout.write(self.style.SUCCESS(f'Successfully re-seeded {len(objects_to_create)} records!'))