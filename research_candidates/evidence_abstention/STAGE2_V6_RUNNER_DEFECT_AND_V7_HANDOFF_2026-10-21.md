# Aşama 2 — V6 test-koşucu tespit hatası ve V7 devri (21 Ekim 2026)

## Bulguyu saklamadan kaydet

V6 teknik tarama koşusu [39664581005](https://github.com/MahmutVezir/dijitalikiz/actions/runs/39664581005) için intake/freeze işi başarılı oldu. İlk tamamlanan vaka artefaktı BugsInPy-matplotlib-3, ZIP SHA-256:

bc03dd025636dda1223d95bfd2780dc21382b0d08dc6038d65047008e0274324

Artefaktın buggy-test.log ve fixed-test.log dosyalarının ikisinde de şu çıktı bulundu:

    bash: line 1: pytest: command not found

İki tarafın da test exit code'u 1, ama buggy_failure_signature_present=false ve fixed_pass_marker_present=false. Dolayısıyla bu bir buggy-fail/fixed-pass çifti değil; ortam/koşucu sorunudur. Runtime Python 3.8.1 ile metadata sürümü eşleşti, fakat test koşucusu bulunmadı.

## Kök neden

Workflow içindeki regex tespiti fazla kaçışlanmıştı: boşluk eşleşmesi için \\s yazıldığı için pytest <argüman> biçimindeki komutlar doğru saptanmadı. Böylece mevcut pytest bootstrap adımı çalışmadı. Bu bir workflow kusurudur; upstream Matplotlib hatasına ilişkin sonuç değildir.

Bu kusuru teşhis etmek amacıyla V6 ilk sekizli batch'in sonuçları incelendiğinden, metodolojik tutarlılık için V6 ilk sekiz adayının tamamı sonuçtan bağımsız olarak doğrulayıcı örneklemden kalıcı çıkarıldı:
- BugsInPy-luigi-4
- BugsInPy-matplotlib-3
- BugsInPy-pandas-3
- BugsInPy-sanic-4
- BugsInPy-scrapy-4
- BugsInPy-spacy-3
- BugsInPy-thefuck-4
- BugsInPy-tornado-4

Bu dışlama, upstream vakaların geçersiz olduğu anlamına gelmez. Yalnızca örneklem seçimini ve iş akışı geliştirme etkisini birbirinden ayırır.

## Düzeltme

- Regex tespiti scripts/evidence_abstention_requires_pytest.py içine taşındı.
- tests/test_evidence_abstention_requires_pytest.py ile pytest komutu, boşluklar, unittest komutu ve hatalı girdi davranışları test ediliyor.
- Cohort workflow'u bu regresyon testini freeze aşamasında çalıştıracak şekilde güncellendi.
- Workflow girişi SCREENING_COHORT_120_V7_2026-10-21.json dosyasına taşındı.
- scripts/build_evidence_abstention_cohort_matrix.py artık önceki 48 maruziyet ID'sini tarihsel kohortlarda reddedecek şekilde güncellendi.

## V7

V7, sabit 487 satırlı BugsInPy kuyruğunda sıralamayı koruyup 48 önceki maruziyet/teknik hata ID'sini atlayarak sonraki 120 adayı alır. V7 metadata-only tarama sırasıdır; rastgele örneklem veya kabul edilmiş veri kümesi değildir.

V7 ilk sekizli batch: BugsInPy-tqdm-4, BugsInPy-youtube-dl-4, BugsInPy-ansible-4, BugsInPy-black-6, BugsInPy-fastapi-5, BugsInPy-httpie-5, BugsInPy-keras-4, BugsInPy-luigi-5.

## Kapanış durumu

- V5 pipeline doğrulama batch'i: 7/8 otomatik buggy-fail/fixed-pass sinyali; tümü maruziyet nedeniyle dışlandı.
- V6 pipeline-debug batch'i: pytest tespit kusuru bulundu; tüm sekiz aday dışlandı.
- V7 intake: oluşturuldu; yeni CI çalışması bekleniyor.
- Kabul edilmiş bağımsız vaka: 0.
- İki ayrı insan paneli, lisans, kök neden, E1/E2/E3, sızıntı ve ön kayıt kapıları: açık.
- LLM çıkarımı: kapalı ve yapılmadı.

V7 workflow koşusu başarılı olsa bile bu yalnızca teknik hattın daha doğru çalıştığını gösterir. Adaylar için kabul kararı, ham log/patch incelemesi ve bağımsız insan değerlendirmeleri olmadan verilmez.
