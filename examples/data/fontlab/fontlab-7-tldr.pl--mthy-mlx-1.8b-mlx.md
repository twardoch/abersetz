# FontLab 7: Pełny przegląd 20 rozdziałów

Ten dokument zawiera zjednoczony, szczegółowy przegląd 20 rozdziałów możliwości, narzędzi i procesów pracy w FontLab 7.

---

# Rozdział 1: Witaj w FontLab 7

## Wprowadzenie i wymagania systemowe

FontLab 7 to kompleksny, profesjonalny edytor fontów do używania na komputerze, zaprojektowany tak, aby sprostać rygorystycznym wymaganiom projektantów typografii, typografów i inżynierów fontów. Opracowany na nowym silniku w porównaniu z starszymi platformami takimi jak FontLab Studio 5, FontLab 7 oferuje nowoczesny, niedestruktywny proces edycji. Funkcjonuje natywnie na macOS 10.10 (Yosemite) i starszych wersjach, a także na Windows 7 i nowszych. Aplikacja obsługuje ekrany o wysokiej rozdzielczości i idealnie integruje się z procesami produkcji. W przeciwieństwie do poprzedniej wersji, która polegała na oddzielnych plikach dla różnych formatów, FontLab 7 wprowadza zunifikowany format pliku `.vfc` (FontLab Document), który przechowuje wszystkie warstwy glyphów, odniesienia i wymienne osie w jednym pliku bazy danych.> [!NOTE] Dla nowych użytkowników oceniających oprogramowanie, FontLab 7 oferuje pełnowymiarową próbę trwałą trwającą 30 dni. W okresie próby wszystkie profesjonalne narzędzia – w tym generowanie fontów, kompilacja funkcji OpenType i skryptowanie w Pythonie – pozostają w pełni aktywne bez znaczników wodnych czy ograniczeń projektowych.

## Pozycja i możliwości w branży

Jako standard w branży typograficznej cyfrowej, FontLab 7 jest używany przez duże firmy produkujące typy i niezależnych projektantów do tworzenia wszystkiego – od pojedynczych kształtów wyświetleń ciężkości do dużych, wielorzędowych rodzin fontów zmiennych. Edytor zapewnia bezprzykładne narzędzia rysowania optymalne do precyzyjnego projektowania wektorowego. Projektowcy mogą manipulować krzywymi Bézier z zaawansowanym kontrolą nad ciągłością węzłów (w tym dopasowywaniem krzywych G2), przesuwać punkty wzdłuż konturów bez zmiany geometrii krzywych oraz równoważyć elementy kontrolne, aby zapewnić optymalną jakość konturu. Środowisko rysowania obsługuje zarówno krzywe PostScript (kubiczne Bézier), jak i TrueType (kwadratowe Bézier), umożliwiając programistom konwersję między typami krzywych bez utraty jakości.

FontLab 7 oferuje natywny, wieloskładnikowy wsparcie. Zawiera kompleksowe narzędzia do systemów projektowych obejmujące zestawy znaków łacińskich, cyrylicyjskich, greckich, arabskich, hebrajskich, indyjskich oraz chińsko-japońskich i koreańskich (CJK). Oprócz tradycyjnych formatów, FontLab 7 jest liderem w nowoczesnych technologiach fontów, oferując solidne możliwości w zakresie:

- **Fontów zmiennych (OpenType Font Variations):** Bezpośrednia edycja osi przestrzeni projektowej, masterów i kompatybilności interpolacji, z wizualnymi wskaźnikami do dopasowywania konturów.
- **Fontów kolorowych:** Wsparcie dla formatów OpenType-SVG, COLR/CPAL oraz CBDT/CBLC bitmap.
- **Inteligentnej interpolacji:** Precyzyjne zarządzanie projektami masterów, metrykami i klasykerningu w wielowymiarowych przestrzeniach.

## Metryki i mechanika projektowaProjektowanie wysokiej jakości czcionek wymaga starannego uwzględnienia odstępów. FontLab 7 obsługuje boczne nakładanie, szerokości postępujące i kerning z zaawansowaną precyzją matematyczną. Użytkownicy mogą dynamicznie łączyć metryki za pomocą wzorów, co gwarantuje, że zmiany w konturze glyphu natychmiast aktualizują relacje odstępów. Integrowane narzędzia Metrics i Kerning działają w środowisku edytora tekstu, ułatwiając czasowe sprawdzanie złożonych kombinacji pisma. Dzięki temu projektanci czcionek mogą bezpośrednio dostosowywać boczne nakładanie i pary kerning w kontekście, używając kerningu opartego na klasy, aby efektywnie zarządzać tysiącami par.

## Ewolucja i ciągłe aktualizacje

W przeciwieństwie do statycznych cykli rozwoju starszych narzędzi, FontLab 7 jest narzędziem ciągle ewoluującym. Znaczące ulepszenia, nowe polecenia, optymalizacje wydajności i ulepszenia ścieżek pracy są wprowadzane w małych wersjach (np. 7.1, 7.2 i kolejne dot-releases).

> [!IMPORTANT] Aby utrzymać kompatybilność z ewoluującymi systemami operacyjnymi i specyfikacjami czcionek, użytkownicy muszą regularnie przeglądać notatki dotyczące małych wersji. Te notatki stanowią główną dokumentację nowych funkcji i zmienionych skrótów klawiszowych.# Rozdział 2: Projektowanie i dostosowywanie interfejsu użytkownika

## Paradomy układu pracy

FontLab 7 posiada bardzo elastyczny interfejs użytkownika zaprojektowany tak, aby obsłużyć różne style projektowe i konfiguracje z wieloma monitorami. W zakładce **Preferencje > Ogólne** można skonfigurować interfejs do działania w jednym z trzech trybów okien:

- **Tryb Jednego Okna / Tabów:** Dokumenty, okna z fontami i okna z glyphami są organizowane jako taby w jednym głównym ramie aplikacji. Dzięki temu przestrzeń pracy jest czysta i unika się nakładania okien.
- **Tryb Okien Uniesionych:** Każde otwarte okno pracy z fontami i glyphami istnieje w niezależnym, uniesionym oknie. Idealne do konfiguracji z wieloma monitorami, umożliwiające przesuwanie rysunków, edytorów metryk i okien wstępnych po ekranach.
- **Okna i Taby Okien:** Hybrydowy sposób, który pozwala na zsunięcie okien razem lub ich uniesienie. Aby zsunąć okno uniesione, użyj **Okno > Zsunięcie > Okno może być zsunięte**, lub połącz je za pomocą poleceń takich jak **Połączyć wszystkie okna** lub **Połączyć z okna fontów**.

## Zsunięcie i grupowanie paneliPaneli w FontLab 7 jest wiele kontekstów, mogą unosić się swobodnie lub przywierać do krawędzi ekranu, okna aplikacji lub innych paneli. Aby przywierać panel, przesuń jego krawędź tytułową w kierunku krawędzi innego panelu lub okna. Jasnoniebieska linia wskazuje na poprawną strefę przywierania, a panel staje się półprzezroczysty podczas przesuwania. Aby stworzyć grupę paneli z tabami, przesuń panel bezpośrednio nad innym panelem. Panel, który przywiera, jest wyróżniony na niebiesko; opuszczenie panelu łączy je, a ich tytuły pojawiają się na dole grupy.

> [!NOTE] Gdy panel jest uniesiony, kwadratowy przycisk w górnej prawym rogu określa jego zachowanie przywierania:
>
> - **󰀞 (Plus):** Może przywierać do krawędzi ekranu lub między panelami, może być grupowany, ale nie może przywierać wewnątrz okna.
> - **󰀟 (Inverted L):** Zachowanie domyślne. Panel może przywierać do dowolnej krawędzi okna lub panelu, krawędzi ekranu lub do grupy z innymi.
> - **󰀝 (Empty):** Panel jest zamknięty w stanie uniesienia i nie może przywierać ani być grupowany.

## Bara właściwości wrażliwych na kontekst

Bara właściwości znajduje się na górze okien Font i Glyph, zapewniając natychmiastowy dostęp do ustawień.- **Okno Font (Statyczne):** Pasek właściwości pozostaje niezmienny. Zawiera przełączniki dla Sidebar (`◧`), Table (`▦`) i List (`◨`), a także opcje tytułów komórek, potencjalne filtry (Encoding, Category, Script), selectory sortowania, wyróżnienia flag/mark i pole wyszukiwania.
- **Okno Glyph (Dynamyczne):** Środkowa część paska dostosowuje się do aktywnego narzędzia (takiego jak Contour, Zoom, Guides, Metrics czy Kerning) lub aktualnej selekcji. Części lewa i prawa pozostają statyczne, pokazujące przełączniki dla Content Sidebar, Spacing Controls, Kerning, Mark Attachment, aktywnych selectorów warstwy/mastera oraz narzędzi wyszukiwania/wyróżnień.

## Odkrywanie funkcji: Pomoc szybka i workspaces

FontLab 7 zawiera wbudowany system **Pomocy szybkiej**. Przesunięcie kursora nad dowolnym kontrolą UI i naciskanie `++F1++` (lub `++Fn+F1++`) wyświetla kompresowane oświadczenie. Naciskanie `++F1++` permanentnie włącza ten tryb. Aby uzyskać dogłębną kontekst, naciskanie `++Shift+F1++` otwiera specjalny **Panel Pomocy**.

Aby optymalizować swoje środowisko, skonfiguruj swoje ustawienia i wybierz **Window > Workspaces > Save Workspace**. Możesz zapisać specjalne konfiguracje dla konkretnych procesów pracy:

- **Pracownia rysunku:** Priorytetem są paneli Canvas, Layers i Element.
- **Pracownia metryk:** Podkreślone są kontrolery rozmieszczenia i panel Przybliżenie.
- **Pracownia kodowania funkcji:** Skupiona na panelach Funkcje i Wyświetlania.

> [!TIP] Przywróć te prace poprzez **Window > Workspaces** lub użyj skrótów klawiszowych `++Opt+Cmd+1++` do `++Opt+Cmd+6++` (macOS), aby natychmiast zmienić układy.

---

# Rozdział 3: File’y i formaty fontów

## Natywne formaty pracy

FontLab 7 wykorzystuje dwa natywne formaty plików do pracy: **VFC (FontLab Compact)** i **VFJ (FontLab JSON)**. Te formaty pełnią rolę głównych dokumentów produkcyjnych (podobnie jak plik PSD w Adobe Photoshop), zachowując wszystkie własnościowe elementy projektowe – w tym noty glyphów, piny, odniesienia do elementów, smart corners i układy pracy – które formaty kompilowanych są pomijane.- **VFC (.vfc):** Proprietary, cross-platform format binarowy optymalny do maksymalnej szybkości, szybkiego czytania i przechowywania na dyskach kompaktowych. Jest to zalecany format do codziennej pracy projektowej.
- **VFJ (.vfj):** Reprezentacja tekstowa formatu native’owego przy użyciu struktur JSON. Chociaż są większe od plików VFC, VFJ są czytelne dla człowieka, co czyni je doskonałymi do analizy opartej na skryptach, automatycznych procesach pracy i kontroli wersji.

> [!TIP] W zakładce `Preferences > Save Fonts`, wyłącz policzek **Session** podczas zapisywania plików VFJ. To usuwa chwilowe daty modyfikacji z pliku, co daje czyste różnice kodów (diff) przy śledzeniu plików źródłowych za pomocą git lub innych systemów kontroli wersji. Włącz **Prettify VFJ**, aby wygenerować formatowaną indentację dla czytelności człowieka.

## Otwieranie, zapisywanie i eksportowanie

FontLab rozróżnia środowisko pracy od finalnego dostarczenia.- **Otwieranie:** Użyj `File > Open Font(s)...`, aby otworzyć pliki. Otwieranie plików nienative (takich jak zkompilowane pliki OTF/TTF) uruchamia wewnętrzny proces konwersji. Możesz skonfigurować preferencje konwersji w `Preferences > Open Fonts`, aby kontrolować, jak obsługiwane są mapowanie CID, zaokrąglenie konturów, strefy alinhowania i funkcje OpenType Layout.
- **Zapis:** Komendy takie jak `File > Save Font` (`Cmd+S`) zapisywane są wyłącznie w formatach VFC lub VFJ, zachowując historię edycji i ustawienia pracy.
- **Eksport:** Aby wygenerować używane fonty, użyj `File > Export Font(s)...`. Kompiluje źródło do formatów gotowych do dystrybucji, konwertując specjalistyczne elementy (takie jak Smart Corners) do standardowych krzywych Bezier.

## Konfiguracje zabezpieczeń i automatycznego zapisu

Aby zapobiec utracie danych, FontLab 7 oferuje solidne mechanizmy zabezpieczeń wieloskładnikowych i automatycznego zapisu skonfigurowane za pomocą `Preferences > Save Fonts`.

Podczas zapisywania nad istniejącym plikiem możesz wybrać, jak aplikacja będzie obsługiwać poprzednią wersję:

1. **Prześlij na nowo:** Zastępuje istniejący plik bezpośrednio.
2. **Prześlij do śmieci:** Wysyła starszą wersję do systemowego kosza.
3. **Zmień nazwę:** Dodaje datę i godzinę do poprzedniego pliku.Włączając **Zapisz pliki zaporowe do podprawy**, pliki zaporowe zmienionej nazwy są automatycznie przechowywane w katalogu `.backup` obok pliku głównego. Dodatkowo, włączenie **Autosave** utrzymuje tło repliki Twojego aktywnego miejsca pracy. W przypadku awarii FontLab poprosi Cię o przywrócenie tych projektów zapisanych automatycznie po ponownym uruchomieniu; są bezpiecznie usuwane po czyskim, ręcznym zapisaniu i zamknięciu.

## Interoperacyjność i Formaty Distribucji

FontLab 7 zapewnia wysoką jakość interoperacyjności w całej branży fontów:

- **Formaty na komputerze:** Eksportuje standardowe formaty **OTF** (PostScript/CFF) i **TTF** (TrueType).
- **Web Fonts:** Eksportuje **WOFF** i **WOFF2**, przy czym WOFF2 wykorzystuje kompresję Brotli od Google, co zmniejsza rozmiar pliku o ponad 30%.
- **Wymiana źródeł:** Bezproblemowe wymienianie plików z innymi edytorami za pomocą XML-owych **UFO** (Unified Font Object) lub natywnego formatu **.glyphs** (podtrzymuje pipeline Glyphs 2 i 3).
- **Color OpenType:** Podtrzymuje wszystkie główne formaty kolorów, w tym **OpenType SVG** (gradycemiki wektorowe/bitmap), **COLR** (kolorów wektorowych w warstwach) od Microsofta oraz **sbix** od Apple lub **CBDT** (fonty kolorowe oparte na bitmapach) od Google.

---# Rozdział 4: Panel sterowania Okna Fontów

Okno Fontów jest centralnym centrum dowodzenia, służącym do zarządzania, organizowania i audytowania plików z fontami. Gdy tworzysz nowy font lub otwierasz istniejący plik, FontLab wyświetla twoje glyphy w strukturalnej interfejsie sieci komórek, oferując kompleksowy przegląd przestrzeni projektowej.

## Interfejs sieci komórek

Główna część Okna Fontów składa się z wykresu glyphów, gdzie każda komórka reprezentuje pojedynczy glyph. Istniejące glyphy pokazują swoje kontury na białym tle, natomiast puste miejsca na glyphy są wyświetlane na szarym tle z lekkim szarym szablonem. Te szablony służą jako wizualne wskazówki dla oczekiwanych znaków, ale nie zawierają rzeczywistych danych konturowych.

Aby dostosować sieć do różnych procesów projektowych, możesz dostosować wymiary komórek w Dolnym panelu za pomocą przycisków szerokości komórek – od wąskich do bardzo szerokich (stosunek 16:9), co jest idealne dla ligatury i pism kaligraficznych. Dodatkowo menu Kolumn (Cols) oferuje ustawione rozmiary komórek (8, 16, 24, 32 lub 64 kolumn na wiersz) lub tryb „Flex” do swobodnego powiększania i zmniejszania za pomocą skrótów klawiszowych do powiększania (`Cmd+=` i `Cmd+-`).> [!TIP] Paski menu Listy (◨) oferują alternatywę w stylu arkuszu kalkulacyjnym do sieci, wyświetlając modulowalne kolumny dla sidebearings (LSB/RSB), szerokości przodu i innych metadanych komórki. Dwukrotnym kliknięciem na dowolną wartość w widoku Listy umożliwia się natychmiastowe edycję w tym samym okienku.

## Nawigacja, Metadane i Flagowanie

Nawigacja w sieci okna Font jest intuicyjna: kliknięcie służy do wyboru glyfu, przesuwanie do wyboru ciągłych obszarów, lub trzymanie `Cmd` (macOS) / `Ctrl` (Windows) do wyboru nieprzyległych komórek. Jedna komórka pozostaje aktywna jako „obecny” glyf, wyróżniona na niebiesko. Dwukrotnym kliknięciem otwiera się glyf w Okienku Glyfów do rysowania.

Każda komórka wyświetla kluczowe metadane w jej tytule, które mogą zawierać nazwę glyfu, kod Unicode, indeks glyfu lub inne dane kodowania. Jeśli nazwa glyfu nie pokrywa się z przypisanym jej kodem Unicode, FontLab wyświetla żółty wskaźnik jako ostrzeżenie.Aby zarządzać złożonymi projektami, można przypisywać flagi kolorowe (wcześniej nazywane „Markami”) za pomocą paska właściwości, menu kontekstowego lub Sidebar. Te flagi kolorują tło lub napis komórki. W sekcji Flag w Sidebar można zobaczyć wszystkie unikalne flagi kolorowe grupowane według wartości koloru numerologicznego, wraz z liczbą glyphów przypisanych do każdej flagi.

> [!NOTE] Naciskanie klawisza Space w dowolnej komórce glyphów otwiera tymczasowy okienek informacji glyphów pokazujący szczegółowe metryki, właściwości Unicode i tagi.

## Filtrowanie i wyszukiwanie w tabeli

FontLab oferuje solidne metody filtrowania wykorzystujące pasek właściwości i Sidebar, aby izolować specyficzne zestawy glyphów:

- **Kodowania**: Filtrowanie według standardowych i zewnętrznych plików kodowania (`.enc`), wyświetlając sloty w kolejności kodowania.
- **Bloki Unicode**: Filtrowanie według standardowych bloków Unicode (Range’ów) w celu systematycznego dodawania znaków.
- **Kategorie**: Filtrowanie według grup typograficznych, takich jak wielkie litery (`_uc_`), małe litery (`_lc_`), znaki interpunkcyjne lub liczby (`_fig_`).
- **Codepages**: Filtrowanie według platform docelowych lub starych kodowań (np. Win-1252, MacOS Roman).
- **Indeks**: Sortowanie i filtrowanie glyphów według wartości Glyph Index (GID). Gdy jest aktywne, manualne sortowanie jest wyłączone.Szybka pasek wyszukiwania w górnej prawym rogu pełni funkcję filtra specjalnego. Możesz wyszukiwać według nazwy glyphu, nazwy znaków Unicode, zakresu lub pisma. Obsługuje wyszukiwania z wieloma podciągami (np. wpisanie `la ca` znajduje „Latin Capital”, a `cu sy` znajduje „Symboly walut”). Możesz zapisać wyniki wyszukiwania jako filtry, przesuwając je do Sidebar Bookmarks lub kliknięciem przycisku `+` w sekcji Historia wyszukiwań.

---

# Rozdział 5: Nawigacja w Okienku Glyph

Okno Glyph (GW) jest głównym miejscem pracy w FontLab 7, w którym rysujesz, edytujesz, przypisujesz, kernujesz i podsuwasz pojedyncze glyphy lub większe ciągi glyphów. Dwukrotnie kliknięcie na dowolny komórkę glyphu w Okienku Font otwiera Okno Glyph, umieszczając wybrany glyph w środku tła edycji.

## Tło edycji i kontrola widoku

Tło edycji wyświetla kształty glyphów wraz z metrykami, wytycznymi i strukturami konturów. Kontrola widoku jest kluczowa dla szczegółowego projektowania wektorowego:- **Przesuwanie:** Użyj `Cmd + Plus` i `Cmd + Minus` (macOS) lub `Ctrl + Plus` i `Ctrl + Minus` (Windows), aby przesuwać w górę i w dół. Naciśnij `Cmd+1`, aby zobaczyć obraz w skali 100%, `Cmd+2`, aby przesunąć na wybrany element, a `Cmd+0`, aby dopasować aktywny symbol lub ciąg tekstu do okna. Możesz również trzymać `Cmd+Space` i przesuwać, aby dynamicznie przesuwać.
- **Ustawienia:** W _Ustawienia > Okno Symboli_, możesz dostosować domyślny współczynnik powiększenia, rozmiar kroku powiększania, szybkość przesuwania oraz to, czy powiększanie skupia się na wskaźniku myszy.

## Miary, Wskazówki i Współrzędne

Aby utrzymać spójność typograficzną, Okno Symboli_ zapewnia precyzyjne narzędzia wizualne i miary:

- **Rulerzy:** Przełączaj rulerzy używając `Cmd+R` (`View > Rulers`). Pokazują one współrzędne tablicy w odniesieniu do linii podstawowej, wysokości x i boków (określając bok lewy i granicę szerokości postępu).
- **Wskazówki:** Przesuń z rury poziomej lub pionowej, aby utworzyć wskazówki. Wskazówki lokalne należą do aktywnego glyphu, natomiast globalne wskazówki obowiązują na całej czcionce. Kliknij dwa razy na wskazówkę, aby edytować jej nazwę, dokładne położenie, kolor lub wyrażenia matematyczne w właściwościach wskazówki.
- **Współrzędne:** FontLab 7 obsługuje zarówno współrzędne całkowite, jak i dzielone (wykładnik dwójny). Wybierz współrzędne dzielone, aby zachować gładkość krzywej Bezier i ciągłość węzła G2 w ramach zmian głównych, a następnie zaokrąglij je za pomocą `Contour > Round Coordinates` dla finalnych eksportów czcionek.

## Paski kontroli i Pasek właściwości

Interfejs wokół tablicy dostosowuje się do Twojego procesu pracy:- **Bara własności:** Umieszczona na górze okna, wyświetla kontrolki związane z kontekstem dla aktywnego narzędzia (np. współrzędne węzłów, kąty uchwytów lub opcje alinhowania).
- **Boczka treści:** Zawiera listę główną, aktywne warstwy tekstu oraz szybki dostęp do edycji wskaźników.

## Zakres edycji: Ekskluzywny vs. Wspólny

Domyślnie operacje edycji są wyłącznie dla aktywnego elementu na obecnej warstwie głównej. Aby jednocześnie edytować inne obszary, można dostosować zakres edycji:

- **Edycja między elementami:** Gdy jest włączona (`Edit > Edit Across Elements`), można wybrać i edytować węzły należące do różnych elementów wektorowych w tym samym glyphie.
- **Edycja między glyphami:** Przekręć to (`Alt+Cmd+E`) aby edytować kontury dowolnego glyphu widocznego w ciągu tekstu, a nie tylko aktywnego.
- **Edycja między warstwami:** Gdy jest aktywna, zmiany mogą być zastosowane jednocześnie na kilku warstwach głównych lub warstwie Mask.

> [!TIP] Użyj `Shift+Alt+Space`, aby przełączyć _Detale między glyphami_. Gdy jest wyłączone, nieaktywne glyphy wyświetlają się jako czyste, wypełnione sylwetki, ukrywając rozpraszające uwagę struktury węzłów.

## Tryb tekstowyPrzejdź do narzędzia tekstowego (`T`) aby wejść w tryb tekstowy. To przekształca tablicę rysunkową w interaktywny edytor tekstu:

- **Wprowadzanie bezpośrednie:** Wprowadzaj znaki Unicode bezpośrednio na tablicę, aby zobaczyć, jak są rozmieszczone i jakie są spacje i kerny.
- **Notacja Glyphtext:** Wprowadzaj glyfy pod nazwą za pomocą składni `/name` (np. `/A/B/C/d.sc`) lub punktów kodów heksadecymalnych (`\u0041`).
- **Wyjście:** Naciśnij `Esc`, aby wrócić do poprzedniego narzędzia rysowania lub edycji.

---

# Rozdział 6: Podstawowe narzędzia rysowania wektorowego

FontLab 7 zawiera potężny zestaw narzędzi rysowania wektorowego, specjalnie zaprojektowanych do projektowania typografii i inżynierii fontów. Rysowanie konturów glyfów wymaga precyzyjnego kontrolowania krzywych Bézier, ciągłości węzłów i geometrii kształtów. Ten rozdział omawia główne narzędzia do tworzenia i edycji konturów: narzędzia Pencil, Pen i Rapid, a także pierwiastki geometryczne i techniki wstawiania węzłów.

## Narzędzie Pencil (N)

Narzędzie **Pencil** jest optymalne do rysowania swobodnym ruchem i szybkiego prototypowania. Pozwala projektantom rysować ścieżki naturalnie, bez konieczności ręcznego umieszczania pojedynczych punktów kontrolnych Bézier. FontLab automatycznie konwertuje rysunek swobodnym ruchem w gładkie krzywe Bézier i odcinki prostych linii.- **Rysowanie ręczne:** Przesuń kursorem, aby narysować krzywe. Naciśnij `Alt`, aby rysować linie prostą, lub `Alt+Shift`, aby ograniczyć ścieżkę w poziomie lub pionie.
- **Zamknięcie ścieżek:** Przenieś kursor z powrotem do węzła początkowego; niebieski okrąg wskazuje, że uwolnienie myszy zamknie kontur.
- **Edycja istniejących konturów:** Dzięki narzędziom _Piór i ołówek, które mogą być używane nad konturami_ w ustawieniach, rysowanie nad istniejącym konturem z węzła do węzła pozwoli na bezproblemowe zastąpienie lub rozszerzenie tej części.

> [!TIP] Użyj narzędzia Ołówek z tabletem rysunkowym, aby szybko narysować importowane skany tła lub analogowe rysunki przed ręczną korektą węzłów.

## Narzędzie Piór (P)

Tradycyjne narzędzie Bézier **Piór** oferuje absolutną kontrolę manualną nad umieszczaniem węzłów i kierunkiem krawędzi wektorowych, co jest kluczowe dla uzyskania czystych konturów i idealnej ciągłości węzłów (takich jak gładkość G1 i G2).- **Tworzenie węzłów:** Kliknij, aby umieścić węzeł rogowy. Kliknij i przesuń, aby stworzyć gładki węzeł z symetrycznymi punktami kontrolnymi Béziera.
- **Dostosowanie uchwytów:** Trzymaj `Alt`, przesuwając, aby zmienić ustawienie uchwytów i stworzyć punkt rogowy z niesymetrycznymi uchwytami. Trzymaj `Shift`, aby ograniczyć kąty uchwytów do kroków 45 stopni.
- **Zamknięcie i zakończenie:** Kliknij w węzeł początkowy, aby zamknąć pętlę, lub naciśnij `Esc`, aby pozostawić kontur otwarty.

## Narzędzie Rapid (5)

Narzędzie **Rapid** to inteligentny narzędzie rysowania klikniękowe, które automatycznie określa umieszczenie węzłów i uchwytów na podstawie miejsca kliknięcia. Rysuje krzywe Béziera kwadratowe z specjalną interfejsem, który automatycznie przekształca się w krzywe Béziera trójkątne podczas zmiany narzędzia.- **Umieszczenie węzłów:** Kliknięcie służy do dodania prostego węzła; dwa kliknięcia (lub `Ctrl+Kliknięcie`) służą do umieszczenia gładkiego węzła. `Cmd+Alt+Kliknięcie` umieszcza węzeł tangensowy.
- **Kontrola napięcia:** Wykresy zakrzywione tworzone są przy użyciu domyślnego napięcia określonego w informacjach fontu. Wyższe wartości napięcia powodują wykresy superelipsyczne.
- **Interaktywne dostosowania:** Przesuwanie dowolnego węzła lub punktu kontrolnego podczas rysowania pozwala natychmiast zmodyfikować ścieżkę. Dwa kliknięcia dowolnego węzła umożliwia przejście między typami połączeń gładkich a kątowych.

> [!WAŻNE] Włączenie _Rapid tool remembers last state_ w Preferencjach pozwala ci ciągle umieszczać węzły tego samego typu bez konieczności dwukrotnie klikania przy każdym wykresie.

## Kształty elementów (I i O)

Do konstrukcji geometrycznych glyphów FontLab zawiera narzędzia **Rozety** (`I`) i **Elipsy** (`O`).- **Gesty rysowania:** Przesuń, aby zdefiniować granice kształtu. Trzymaj `Shift`, aby ograniczyć się do kwadratu lub kółka, a `Alt`, aby rysować od środka.
- **Wprowadzanie liczbowe:** Kliknij raz na canvas, aby otworzyć okno dialogowe „Dodaj prostokąt” lub „Dodaj owal”, a następnie wprowadź precyzyjne wymiary.
- **Geometryczne vs. zakrzywione:** W pasku właściwości przejdź między tradycyjnymi geometrycznymi elipsy a zakrzywionymi elipsy, które uwzględniają parametr napięcia czcionki.

## Wstawianie węzłów na ścieżkach

Dodawanie węzłów do istniejących ścieżek jest kluczowe dla dopracowania ścieżek i dodawania szczegółów:

- **Z narzędziami pióra/rapidy:** Przesuń się nad aktywnym odcinkiem i kliknij, aby wstawić węzeł rogowy (lub kliknij dwa razy z narzędziem rapidy, aby uzyskać gładki węzeł).
- **Z narzędziem konturu (`A`):** Kliknij dwa razy na dowolny odcinek, aby wstawić nowy węzeł bez modyfikacji geometrii istniejącej krzywej.

---

# Rozdział 7: Zaawansowane edycja punktów i węzłów

## Typy węzłów: Róg vs. Gładki

W FontLab 7 kontury są definiowane przez krzywe Bézier i dwa główne typy węzłów, które określają, jak łączą się segmenty ścieżek.- **Węzły kątowe**: Wskazane przez czerwone, kwadratowe symboly. Węzły kątowe (lub ostre) tworzą nierówny kąt między dowolnymi dwoma odcinkami (prostymi lub krzywymi).
- **Węzły gładkie**: Wskazane przez zielone, okrągłe symboly. Węzły gładkie zapewniają ciągłość styczności. Między dwoma krzywymi są _węzły krzywizny_, które ustawiają rączki równolegle. Między krzywą a prostą linią są _węzły styczności_, które zmuszają rączki do ustawienia się z prostym odcinkiem.

Dwiekietanie węzła przełącza go między węzłem kątowym a gładkim.

> [!UWAGA] Nie ma typu węzła gładkiego do połączenia dwóch prostych odcinków. Jeśli są równoległe, węzeł powinien być usunięty, aby utworzyć jeden odcinek.

## Węzły inteligentne: Sługa i Genius

Węzły inteligentne to specjalne właściwości przypisane węzłom, służące do automatyzacji rysowania i śledzenia krzywych.

### Węzły sług

Węzeł sługa ma swoje współrzędne X, Y lub oba związane z sąsiednimi węzłami nie-sług. Gdy przesuniesz sąsiedni węzeł, pozycja węzła sług jest interpolowana, a jego rączki skalowane proporcjonalnie. Jest to idealne do utrzymania proporcji w kształtach zaokrąglonych. Aby to przypisać, kliknij prawym przyciskiem w węzeł i wybierz **X-Sługa** lub **Y-Sługa** z menu kontekstowego.

### Węzły geniusza

Węzły Genius zawsze utrzymują ciągłość krzywizny G2 (nieskończenie gładkość). W przeciwieństwie do ciągłości G1, która tylko ustawia rączki równolegle, ciągłość G2 zgadza się z tempem zmiany krzywizny po obu stronach węzła. Gdy dostosowujesz rączki węzła Genius, FontLab automatycznie przesuwa pozycję węzła wzdłuż ścieżki, aby utrzymać tę idealną krzywiznę G2.

> [!TIP] Użyj **View > Show > Curvature**, aby sprawdzić ciągłość G2. Krzywizny będą się zgadzać pod względem wysokości po obu stronach węzła Genius.

## Kierunek ścieżki i wypełnienia

Każdy kontur ma wyznaczony **Punkt Początkowy** (pierwszy węzeł) oraz kierunek ścieżki, który może być w kierunku wskazówek zegara lub przeciwnie.

- **Punkt Początkowy**: Wskazany przez szary strzałkę kierunku, gdy jest włączone **View > Show > Contour Direction**.
- **Zasady owinięcia**: Kontury PostScript (Type 1) wymagają, aby ścieżki w kierunku przeciwnym do wskazówek zegara były wypełnione (czarne), a ścieżki w kierunku wskazówek zegara nie były wypełnione (puste/otwory). Kontury TrueType stosują odwrotną zasadę.

Chociaż FontLab 7 automatycznie koryguje kierunki ścieżek i rozwiązuje pokrywania podczas eksportu, możesz ręcznie odwrócić kierunki konturów lub zmienić punkt początkowy, klikając prawym przyciskiem na węzeł i wybierając **Make Start Point**.## Mechanika selekcji

Precyzyjne edycja węzłów jest niezbędna, ponieważ zmiana konturów bezpośrednio zmienia szerokość postępu i boki znaku. Wymaga to zrozumienia, jak FontLab rozróżnia węzły i jak radzi sobie z selekcją.

- **Selekcja indywidualna**: Kliknij bezpośrednio w węzeł lub bok. Kliknij przytrzymując Shift, aby dodać lub usunąć punkty z selekcji.
- **Selekcja marque**: Przesuń prostokąt nad tłem. Jego działanie jest kontrolowane przez `Preferencje > Edycja > Selekcja marque ignoruje boki podczas selekcji węzłów`. Jeśli jest włączona, przesunięcie nad oba węzły i boki selekcjonuje tylko węzły. Jeśli marque obejmuje tylko boki, są one wybrani.
- **Selekcja lasa**: Trzymaj **Alt** podczas przesuwania, aby narysować swobodny lasa, selekcjonując wszystkie węzły i boki w nim znajdujące się.

> [!IMPORTANT] Gdy `Selekcja marque ignoruje boki` jest aktywna, użycie **Shift-marque** do wyłączenia selekcji nadal wyłączy wszystkie zabrany elementy, czy to węzły, czy boki.

---

# Rozdział 8: Manipulacja segmentami i linie Tunni

Modyfikacja konturów w FontLab 7 wymaga zrozumienia geometrii ścieżek, ciągłości węzłów i zachowań przycisków. Ścieżki wektorowe składają się z węzłów i krzywych Bezier. Regulacja długości i kątów przycisków wpływa na napięcie i krzywiznę krzywych, co wpływa na gładkość przejść między segmentami.

## Edycja symetryczna za pomocą linii Tunni

Podczas edycji krzywych definiowanych przez dwa przyciski kontrolne utrzymanie równowagi napięcia jest trudne. FontLab 7 rozwiązuje to za pomocą **linii Tunni** – wyimaginowanych niebieskich kresek z punktami łączących odpowiadające sobie przyciski Bezier w segmentach krzywych. Pozwalają one na jednoczesne regulację napięcia i proporcji przycisków.

Aby włączyć lub wyłączyć linie Tunni, naciśnij `L` lub wybierz **View > Tunni Lines**. Przesunięcie kursora między przyciskami wyświetla linię Tunni i jej centralny punkt kontrolny (duży niebieski punkt).- **Edycja symetryczna:** Przesuń linię Tunni lub trzymając `Shift`, przesuń punkt kontrolny, aby poruszyć oba przyciski w synchronizacji.
- **Edycja asymetryczna:** Przesuń punkt kontrolny bez `Shift`, aby dostosować tylko jeden przycisk.
- **Korekty klawiaturą:** Wybierz linię Tunni i naciśnij `Alt` z strzałkami:
  - `Alt + Left/Right` przesuwa punkt Tunni równolegle, wydłużając jeden przycisk, a skracając drugi.
  - `Alt + Up/Down` przesuwa go ortogonalnie, zwiększając lub zmniejszając napięcie krzywej.
- **Edycja batchowa:** **Contour > Edit Tunni Lines** (`Cmd + Alt + L`) aktywuje linie Tunni dla wybranych segmentów; naciśnij `Esc`, aby wyłączyć.

> [!NOTE] Korekta napięcia za pomocą linii Tunni pomaga zachować ciągłość krzywizny G2, co jest kluczowe dla gładkich przejść krzywych.

## Modele usuwania węzłów i segmentów

FontLab 7 oferuje dwa różne modele usuwania węzłów i segmentów: zachowanie krzywej i awulsja ścieżki.- **Usunięcie z zachowaniem krzywej (Backspace):** Usuwa wybrany węzeł lub rąbek, zachowując zamkniętą krzywą. FontLab ponownie oblicza pozostałe rąbki, aby przybliżyć pierwotny kształt ścieżki.
- **Usunięcie ścieżki (Delete):** Usuwa węzeł i rozrywa krzywą, pozostawiając otwarte końce.
- **Usunięcie segmentu:** Naciskanie `Backspace` usuwa segment i jego węzły, ale zachowuje zamkniętą krzywę. Naciskanie `Delete` usuwa tylko segment, pozostawiając końcowe węzły nienaruszone, ale rozrywając krzywę.

## Narzędzie Nożyczek i Krzywki z pętlą

**Narzędzie Nożyczek** (`Q`) rozłącza węzły, dzieli ścieżki i zarządza przekryciami.

- **Rozłączenie:** Kliknięcie w węzeł rozrywa krzywę i wydłuża sąsiednie segmenty.
- **Uwięzienie tuszu:** Kliknięcie klawiszem Shift w węzeł duplikuje go i rozdziela go w odległości określonej w **Font Info > Font Dimensions > Szerokość uwięzienia tuszu**.
- **Krzywki z pętlą:** Kliknięcie klawiszem Alt w ostry węzeł tworzy zamkniętą, samo-załamaną „krzywę z pętlą”. Pętle rozciągające się na obszarach wypełnionych to _wewnętrzne krzywki z pętlą_; te rozciągające się na pustych obszarach to _zewnętrzne krzywki z pętlą_. Pętle te utrzymują odpowiednie liczby węzłów dla fontów zmiennych.

## Filtry uproszczenia krzywejDla automatycznej optymalizacji FontLab zapewnia dwa filtry:

- **Simplifikuje** (`Alt + Cmd + B`): Ułatwia wykresy, usuwa zbędne węzły i dodaje węzły ekstremum. Przekształca krzywe TrueType w PostScript i może zmieniać kształt.
- **Oczyścić**: Usuwa niepotrzebne węzły bez dodawania nowych, utrzymując kształt konturu bliższy oryginalnemu.

> [!TIP] Użyj **narzędzia Eraser** (`2`) do lokalnej uproszczenia poprzez kliknięcie `Ctrl` na węźle, a następnie kliknięcie na inny węzeł na tym samym konturze.

---

# Rozdział 9: Odniesienia do Elementów i Kompozycja

FontLab 7 wykorzystuje elastyczny, obiektowy sposób budowy glyfów poprzez **Elementy**. Zamiast polegać na prostych, płaskich konturach, FontLab pozwala na tworzenie złożonych glyfów za pomocą pojedynczych, ponownie używanych komponentów projektowych. Ten rozdział wyjaśnia mechanikę kompozycji, koncepcję odniesień do elementów i jak zarządzać nimi w projekcie fontu.

## Projektowanie oparte na komponentach i ElementyW profesjonalnym projektowaniu typograficznym glyfy są często składane z oddzielnych elementów – takich jak łuki, serify czy diakryty. W FontLab 7 każdy rysunek wektorowy, obrazek lub pola tekstowe traktowane jest jako **Element**. Warstwa glyfu może zawierać jeden element lub kompozycję wielu elementów.

W przeciwieństwie do standardowych warstw, które oddzielają całe projekty główne (takie jak Regular i Bold) lub przestrzenie koordynacyjne, elementy są strukturalnymi blokami w jednej warstwie. Kompozycja polega na łączeniu tych bloków, aby utworzyć kompletne glyfy, np. łączenie elementu `e` z elementem `acute`, aby stworzyć `eacute`.

## Odniesienia do Elementów vs. Komponenty

Podczas gdy inne edytory fontów używają „komponentów” do łączenia konturów jednego glyfu z innym, FontLab 7 wykorzystuje **Odniesienia do Elementów**. Odniesienie do Elementu to link do elementu źródłowego. Kluczowa różnica polega na tym, że elementy nie muszą istnieć jako samodzielne glyfy w twoim fontie; mogą znajdować się wyłącznie w **Galerii** fontu lub jako elementy niemapowane.

Gdy kopiujesz element i wklejasz go jako odniesienie (używając `Edit > Paste Special > Links` lub `Element > Reference`), tworzysz żywy klon.- **Live Linking:** Edycja krzywych Bezier, ciągłości węzłów (stan G1 lub G2) lub współrzędnych jednego elementu natychmiast aktualizuje wszystkie inne instancje w całym fontie.
- **Transformacje niedestruktywne:** Każda instancja odniesienia może być unikalnie skalowana, obrócona, odwrócona lub przesunięta bez zerwania połączenia z konturami źródłowymi.
- **Indywidualne wskaźniki:** Szerokość postępu i sidebearings kompozytowanego glyphu pozostają dostępne do dostosowania, podczas gdy wewnętrzne umieszczenie odniesienia aktualizuje się dynamicznie.

> [!TIP] Używaj odniesień do elementów dla wspólnych elementów takich jak serify, łodygi czy akcenty diakrytyczne. Zapewnia to spójność stylistyczną i przyspiesza globalne dostosowania projektu.

## Zarządzanie elementami

FontLab 7 zapewnia kilka narzędzi i paneli do organizacji i manipulacji elementami:

### Panel Elementów i lista warstw

**Panel Elementów** wyświetla hierarchiczną strukturę aktywnej warstwy. Tutaj możesz nadawać nazwy elementom, przeglądać ich odniesienia i przekształcać ich kolejność. Przekształcanie elementów zmienia ich stos renderowania, co jest kluczowe dla fontów kolorowych lub powierzchni nakładających się na siebie.

### Panel Galerii

**Panel Galerii** służy jako repozytor wszystkich elementów w czcionce. Możesz przesuwać elementy z płachty do Galerii, aby je zapisać do przyszłego użycia, lub przesuwać je z Galerii do glyphu, aby umieścić odniesienie.

### Rozkładanie odniesień

Jeśli potrzebujesz dokonania unikalnych edycji w przypadku elementu bez wpływania na inne glyphy, musisz go **rozkładać**.

1. Wybierz odniesienie elementu w okienku Glyph.
2. Wybierz `Element > Rozkładać` (lub kliknij ikonę rozkładania w panelu Elementów).
3. Odniesienie zostaje przekształcone w niezależne, lokalne kontury Bezier.

> [!WAŻNE] Rozkładanie jest destruktywne i nie można go cofnąć po zapisaniu pliku. Łącze z elementem nadrzędnym zostaje trwale przerwane.

---

# Rozdział 10: Praca z kolorami i swatchami

FontLab 7 zawiera kompleksową zestaw narzędzi kolorowych zaprojektowanych do zarządzania procesem projektowania i tworzenia wielokolorowych, warstwowych czcionek OpenType. Kolor można zastosować jako metadane do oznaczenia komórek glyphów w interfejsie, lub bezpośrednio do konturów glyphów jako właściwości kreski i wypełnienia wektorowego.

## Organizacja kolorów wizualnych

Kolory są niezbędnym narzędziem organizacyjnym w projektowaniu czcionek. FontLab 7 rozróżnia organizację na poziomie interfejsu (taką jak oznaczanie glyfów w celu śledzenia postępu projektu) od przypisywania kolorów na poziomie konturów (takie jak tworzenie czcionek kolorowych za pomocą tabel SVG lub COLR/CPAL).

## Oznaczanie komórek

Oznaczanie komórek (w FontLab Studio 5 określane jako „oznaczenia glyfów”) umożliwia nakładanie koloru tła i napisu na komórki glyfów w okienku czcionek. Oznaczanie jest doskonałym sposobem kategoryzowania glyfów według statusu, typu (wielkie litery, małe litery, cyfry) lub pisma.- **Zastosowanie flag:** Wybierz komórki glyphów i wybierz jedną z pięciu predefiniowanych kolorów flag (Czerwony, Niebieski, Zielony, Magenta, Cyjan) z nagłówka Okna Fontu lub z podmenu **Flag** w menu kontekstowym.
- **Flagi dostosowane:** Wybierz **Custom...**, aby określić wartość koloru dostosowanego (0–360) za pomocą skalnika lub bezpośredniego wprowadzenia liczbowego.
- **Usuwanie flagów:** Wybierz flagowane glyphy i kliknij **No flag** w nagłówku lub menu kontekstowym.
- **Paski boczne i filtrowanie:** W pasku bocznym Okna Fontu sekcja **Flag** wyświetla wszystkie aktywne flagi wraz z liczbą glyphów przypisanych do każdego. Kliknij flagę w pasku bocznym, aby zfiltrować Okno Fontu. Włącz **Hide Unfiltered Glyphs**, aby widzieć tylko flagowaną część, lub zostaw to wciśnięte, aby grupować flagowane glyphy na górze.
- **Selekcja:** Użyj **Select > Same Flag** z menu kontekstowego, aby wybrać wszystkie glyphy dzielące się flagą aktywnego glypha.

> [!TIP] Flagowanie komórek nie wpływa na wizualne kontury eksportowanego fontu, ale FontLab używa tych metadanych podczas rozwoju do filtrowania, sortowania i przetwarzania batchowego.

## Kontury i wypełnienia konturówW tym projekcie kolorowych fontów można stosować kolory linii i wypełnienia do konturów glyfów. W FontLab 7 kolory są stosowane na poziomie **Elementu**, a nie na pojedyncze kontury lub węzły. Kontury należące do tego samego elementu muszą mieć takie same linie i wypełnienie, ale oddzielne elementy lub odniesienia elementów w jednym glyfie mogą być kolorowane niezależnie.

**Panel Kolorów** (**Window > Panels > Color**) posiada trzy tryby interfejsowe: koło, przycisky sterujące i okno.

- Aby kolorować kontur, kliknij niezapisany okrąg w górnej lewej części panelu, wybierz kolor i kliknij **Apply**.
- Aby kolorować wypełnienie konturu, kliknij zapisany okrąg, wybierz kolor i kliknij **Apply**.
- Aby zastosować kolory grupowo, wybierz kilka elementów w Okienku Fontów. Trzymając `Alt`, kliknij **Apply**, aby przypisać kolor aktualnej warstwie wszystkich wybranych glyfów.

## Panel Swatches

Podczas gdy Panel Kolorów służy jako wybieracz, **Panel Swatches** (**Window > Panels > Swatches**) służy jako repozytor predefiniowanych kolorów, umożliwiając przypisanie spójnych właściwości stylu w całej rodzinie fontów.- **Tryby wyświetlania:** Przełączanie między **Trybem Listy** (pokazuje swatchy z nazwami) a **Trybem Tabelą** (wyświetla zwięzłą sieć ikon kolorów).
- **Tworzenie swatchów:** Mieszaj kolor w Panelu Kolorów, a następnie kliknij przycisk **Dodaj Kolor (+)** w pasku statusowym Panelu Swatchów, aby go zapiszć.

## Zarządzanie Bibliotekami Palet

Zarządzaj grupami swatchów, klikając na ikonę palety w pasku statusowym Swatchów, aby otworzyć dialog **Palety**. Tutaj możesz dodawać, duplikować, zmieniać nazwę lub usuwać palety. Palety personalizowane można zapisać jako pliki `.palettes`, co jest idealne do organizacji kategorii stylu i udostępniania konfiguracji kolorów między różnymi projektami.

> [!WAŻNE] Przy eksportowaniu kolorowych fontów FontLab automatycznie generuje tabele CPAL (paleta kolorów) i COLR, lub tabele SVG, w zależności od profilu eksportu.

---

# Rozdział 11: Importowanie Artefaktów i Autotracing

FontLab 7 oferuje solidne narzędzia do konwersji rysunków fizycznych, obrazów rastrowych i zewnętrznych szablonów wektorowych w precyzyjne kontury glyphów gotowych do edycji. Projektanci typograficzni mogą wybrać bezpośredni import grafiki wektorowej lub wklejanie obrazów bitmapowych, wykorzystując zaawansowane filtry i parametry autotracing, aby generować czyste ścieżki Bezier.## Importowanie ilustracji wektorowych w porównaniu z bitmapowymi

Wsparcie FontLab różni się w zależności od tego, czy pracujesz z ilustracjami wektorowymi, czy z plikami bitmapowymi:

- **Grafika wektorowa (SVG, EPS, PDF, AI):** Możesz importować pliki wektorowe za pomocą `File > Import > Artwork` lub kopiując i wklejając bezpośrednio z edytorów wektorowych. Podczas wklejania FontLab obsługuje zarówno tradycyjny **AICB** (idealny dla czystych ścieżek monochromatycznych), jak i formaty **PDF** (idealne dla złożonych projektów wielokolorowych, maski kliknięcia lub ilustracji z Affinity Designer i Sketch). Okno dialogowe _Paste or Import Artwork_ pozwala wybrać między importowaniem **Elementów i Kolorów** (zachowuje krawędź, wypełnienie i kolor) a **Tylko Konturów** (ignoruje stylizację i automatycznie zaokrągla współrzędne do jednostek całkowitych).
- **Pliki bitmapowe (PNG, JPG, BMP, TIFF):** Obrazy rastrowe są importowane jako elementy tła. Domyślnie 1 piksel w obrazie rastrowym odpowiada 1 jednostce pisma. Dla optymalnej rozdzielczości szkice projektowe powinny być skalowane tak, aby kluczowe wymiary (takie jak wysokość kaptura) odpowiadały docelowej wielkości UPM (np. narysowanie wielkiej litery 'H' na wysokości 700 pikseli dla wysokości kaptura 700 jednostek).> [!TIP] Jeśli twoje dzieła artystyczne w formie wektorów mają współrzędne dzielące, włącz preferencje zaokrąglania współrzędnych, aby automatycznie dopasować ścieżki do siatki czcionek po importowaniu.

## Przygotowanie bitmapów za pomocą panelu obrazu

Przed automatycznym rysowaniem oczyścij swoje rysunki rastrowe za pomocą **Panelu obrazu** (`Window > Panels > Image`). Wybierz element obrazu i zastosuj następujące filtry niezniszczliwe:

- **Usuwanie tła:** Izoluje rysunek z tła papierowego.
- **Usunięcie plam / Redukcja szumu:** Oczyści artefakty skanowania, kurz i zbędne piksely.
- **Zmętnienie Gaussowskie i progi:** Lekko zmętnienie obrazu oraz zastosowanie progów (opartego na jasności, transparentności lub kolorze) wyostrza nierówne krawędzie, przekształcając gradienty pikselowe w kształty wysokiego kontrastu czarno-białe.

## Parametry automatycznego rysowania

Aby przekształcić przygotowany obraz, wybierz go i wybierz `Element > Image > Autotrace...`. Okno dialogowe oferuje przegląd w czasie rzeczywistym oraz trzy kluczowe przyciski sterujące generacją początkowego konturu:1.  **Tolerancja na ślady:** Kontroluje, jak blisko ścieżka podąża za granicami pikseli. Wartość 1 śledzi krawędzie dokładnie, natomiast wyższe wartości śledzą je luźniej, co daje prostsze segmenty.

2.  **Dystans przy dopasowaniu krzywej:** Dopuszczalna błądowość przy przybliżeniu krzywej. Niższe wartości generują więcej węzłów; wyższe wartości dają mniej węzłów i płaskie segmenty krzywych.

3.  **Kąt prostowania:** Określa próg przekształcania krzywych w linie prostą. Wyższe wartości faworyzują punkty kątowe i linie proste.

W zakładce **Wynik śladu**, wybierz między **Kontury PS** (kubiczny Bezier), **Kontury TT** (kwadratowy Bezier) czy **Tylko linie**.

> [!IMPORTANT] Postprocesuj swój ślad, sprawdzając **Węzły w ekstremach**, aby automatycznie umieścić węzły w maksymalnych punktach krzywych w pionie i poziomie, co jest kluczowe dla renderowania i podświetlania.

## Przezwyczynia pracowania z śladem i wskazówki ręczne

Po automatycznym śladowaniu, wybierz **Zachować**, **Usunąć** lub **Przenieść do Maski** obraz źródłowy. Przeniesienie obrazu do warstwy Maski z zmniejszoną przezroczystością (np. 20–30%) pozwala zachować oryginalny rysunek jako szablon wizualny do ręcznego śladowania i precyzyjnych korekt konturów.Dla arkuszy zawierających całe alfabet, umieść zeskanowaną ilustrację na Sketchboard i wybierz `Element > Image > Separate and Trace`. FontLab podzieli arkusz na pojedyncze elementy glyphów przy użyciu ustawień optycznego rozdzielania i automatycznie je zlokalizuje w jednym zleceniu.

---

# Rozdział 12: Zarządzanie warstwami i maskami

## Panel Warstw i Masters

Panel Warstw i Masters (**Window > Panels > Layers & Masters**) jest centralnym centrum do zarządzania wielowarstwowymi konstrukcjami glyphów, projektami masters i pomocniczymi konturemi w FontLab 7. Panel ma uporządkowaną hierarchię: lokalną skrzynek w górze, listę warstw do przesuwania pośrodku, sekcję właściwości do skompresowania i paski statusu na dole.

W liście warstw każdy wpis wyświetla swoje imię, przybliżenie, liczbę elementów składowych oraz kolumny statusu dotyczące widoczności, blokowania, atrybutów warstwy usługowej i wyświetlania wireframe. Informacje wizualne są kodowane kolorem, aby wskazać kompatybilność interpolacji:- **Nazwy w kolorze ciemnym:** Wskazują na warstwy główne czcionek lub glyphów, które przyczyniają się do różnic.
- **Żółty:** Główna warstwa jest w pełni kompatybilna z interpolacją.
- **Czerwony:** Główna warstwa jest kompatybilna, ale porządek konturów lub węzłów różni się.
- **Czerwień blade:** Główna warstwa jest niekompatybilna, wskazując na niezgodne liczby punktów lub konturów.
- **Nazwa szara (`#instance`):** Reprezentuje dynamicznie interpolowaną wirtualną instancję.

## Warstwy główne w porównaniu z warstwami usługowymi i pomocniczymi

FontLab 7 rozróżnia główne warstwy eksportowalne od nieeksportowalnych warstw użytkowych:

- **Warstwy główne:** Definiują granice przestrzeni projektowej dla czcionek zmiennych. Zawierają główne kontury Bézier, punkty odniesienia i szerokości postępu, które są eksportowane do formatów końcowych.
- **Warstwy usługowe:** Aktywowanie atrybutu usługi (`_service`) ukrywa warstwę w Okienku Czcionek i panelu Przybliżenia. Warstwy usługowe nie są eksportowane ani nie uczestniczą w interpolacji.
- **Warstwy tła i zamknięte:** Warstwy mogą być przeniesione na tło (dolne miejsce stosu) lub zamknięte, aby uniknąć przypadkowych edycji wektorowych.
- **Tryb szkieletu:** Rysunki wektorowe wypełnione są wyświetlane jako kontury, przydatne do sprawdzania pokrywających się ścieżek.> [!NOTE] Kliknięcie klawiszem Cmd (`++Cmd++` na macOS lub `++Ctrl++` na Windows) na nagłówku kolumny kolorowych kropek automatycznie przypisuje unikalne kolory wszystkim warstwom, z wyjątkiem warstw mask.

## Operacje i właściwości warstw

W pasku statusu można dodawać warstwy (`++Cmd+Shift+N++`), duplikować je lub usunąć. Sekcja właściwości, przełączana za pomocą paska narzędzi, ujawnia kontrolki przezroczystości (0–100%) oraz przełącznik Auto Layer. Aktywowanie **Auto Layer** blokuje edycję ręczną, a zamiast tego automatycznie generuje kontury glyphu przy użyciu predefiniowanych lub dostosowanych receptur glyphów w FontLab.

> [!TIP] Użyj przycisku **Merge Visible Layers** w pasku statusu, aby połączyć widoczne, nieusługowe warstwy przed spłaszczeniem i eksportem.

## Warstwy mask glyphów

Warstwa mask to specjalna warstwa usługowa powiązana z macierzystą warstą projektu, używana do zachowania tymczasowych stanów wektorowych.- **Tworzenie maski:** Wybierz kontury i wybierz **Tools > Copy to Mask** (`++Cmd+M++`).
- **Edycja maski:** Wybierz **Tools > Edit Mask** (`++Ctrl+H++`) lub kliknij dwa razy na kontury maski. Tło tablicy zmienia kolor, wskazując tryb edycji maski.
- **Interakcje:** Przekręć **View > Snap > Mask**, aby aktywne węzły konturów były precyzyjnie umieszczone wzdłuż wektorów maski. Użyj **Tools > Swap with Mask** (`++Ctrl+Alt+M++`), aby wymienić kontury między głównym konturem a maską.

## System Globalnej Maski

W przeciwieństwie do maski lokalnych, **Globalna Maska** jest szablonem odniesienia na cały font, który jest wyświetlany we wszystkich glyphach i warstwach. Nie pojawia się w panelu Layers i Masters.

- **Tworzenie:** Wybierz kontury w dowolnym glyphu i uruchom **Tools > Copy to Global Mask** (`++Shift+Cmd+M++`).
- **Użycie:** Włącz **View > Show > Global Mask** oraz **View > Snap > Global Mask**, aby projektować szablon i precyzyjnie umieszczać kontury na nim w przestrzeni projektowej.
- **Czyszczenie:** Uruchom **Tools > Clear Global Mask** (`++Shift+Cmd+K++`).

---

# Rozdział 13: Używanie SketchboardaSketchboard to otwarte pole do rysowania w FontLab 7 – nieskończona wirtualna tablica, zaprojektowana do wspierania wczesnych etapów projektowania czcionek. W przeciwieństwie do zorganizowanej Okna Czcionki lub pojedynczych Okien Glyph, które zmuszają elementy do miejsce w sztywnych metrycznych ramach i ścisłych hierarchiach glyph, Sketchboard funkcjonuje jako nieograniczone pole rysunkowe. Pozwala on projektantom rysować, importować surowe elementy, śledzić skanowane dzieła sztuki i formatować próbki do weryfikacji w jednym spójnym miejscu pracy.

## Rysowanie poza siecią czcionek

Na Sketchboard można tworzyć i manipulować geometrią wektorową bez przypisywania jej do konkretnego punktu kodowego Unicode lub ograniczania się standardowymi współrzędnymi czcionek. Ta wolność jest idealna do eksperymentalnego rysowania liter, tworzenia logotypów lub eksploracji koncepcji krzywych Bezier przed ich umieszczeniem w formalnym slotu glyph.Możesz używać pełnego zestawu narzędzi rysowania FontLab – w tym narzędzi Rapid, Pen, Pencil i Brush – bezpośrednio na płótnie. Podczas rysowania możesz dopracowywać węzły wektorowe, zarządzać przyciskami i zapewniać ciągłość węzłów (np. ciągłość krzywizny G1 lub G2), bez konieczności martwienia się o szerokości, boczne odległości czy wymiary pionowe. Gdy jesteś zadowolony z kształtu wektorowego, możesz przekształcić go w element i przesunąć go bezpośrednio do komórki w panelu Font Map, natychmiast promując dzieło sztuki jako standardowy glyph.

> [!TIP] Aby szybko przekształcić serię niepołączonych rysunków na Sketchboard w glyphy, wybierz je narzędziem Element (V) i wybierz **Element > Place As Glyphs > Selected Elements**.

## Okna tekstowe i przykładowe ciągi znaków

Sketchboard jest również solidnym narzędziem do próbkowania i testowania typografii. Wybierając narzędzie Text i klikając w dowolnym miejscu na płótnie, możesz stworzyć okno tekstowe. Te okna tekstowe nie są statycznymi wyświetlaczami; pełnią rolę żywych, pełnie edytowalnych multi-glyphowych przykładowych ciągów znaków, wykorzystujących każdy aktywny font otwarty w FontLab.Każda edycja konturów, bocznych oznaczeń lub kerningu w polu tekstowym aktualizuje natychmiast wszystkie egzemplarze tych elementów graficznych na całym obrazku i w samym fontie. Pola tekstowe obsługują trzy różne tryby wyświetlania:

1. **Ciągły tekst**: Zatrzymuje tekst próbny na jednej linii, idealny do testowania rytmu słów i ustawień nagłówków.
2. **Automatyczne wyświetlanie bloku**: Wyświetla tekst w rozmiarowo zmiennym prostokątnym ramce, aby testować tekstury akapitów.
3. **Widok tablicowy**: Umieszcza każdy znak w osobnej komórce, umożliwiając czyste porównywanie z boku do boku.

> [!NOTE] FontLab automatycznie zapisywaje pola tekstowe powiązane z otwartym fontem w odpowiednim pliku VFC lub VFJ. Jeśli zamkniesz font, pola tekstowe znikną, ale ponownie pojawią się w dokładnie tych samych pozycjach po ponownym otwarciu fontu.

## Importowanie grafik i katalogów

Podczas rozpoczynania projektu od rysunków fizycznych, Sketchboard ułatwia przyjmowanie surowych prac artystycznych. Można importować duże pliki graficzne lub katalogi zekranowanych obrazów za pomocą **File > Import > Artwork**. FontLab obsługuje formaty wektorowe (EPS, SVG, AI kompatybilny z PDF) oraz standardowe obrazy bitmapowe.Po importowaniu można użyć **Element > Image > Separate and Trace**, aby optycznie podzielić skanowaną kartkę z literami na pojedyncze elementy graficzne i automatycznie zmapować je do czystych konturów Bezier.

## Eksportowanie Sketchboarda

Aby udostępnić przykłady lub eksportować układy, można bezpośrednio wydrukować zawartość Sketchboarda za pomocą **File > Export > Window Contents**. Ten polecenie eksportuje tło do formatów PDF lub SVG opartych na wektorach, zachowując nie tylko kształty konturów i mapy kolorów, ale także wskazówki, obszary aliniowania i metryki.

---

# Rozdział 14: Odległości i Sidebearings

Aby zaprojektować funkcjonalny font, odległości są równie ważne jak rysowanie konturów. W FontLab 7 odległości są zarządzane poprzez metryki graficzne horyzontalne, które określają, jak poszczególne znaki się względem siebie umieszczają. Kontrolowanie tego rytmu przestrzennie wymaga jasnego zrozumienia wymiarów horyzontalnych, narzędzia Metrics i systemów dynamicznego łączenia.

## Definicje Metryk Horyzontalnych

Horyzontalne odległości graficzne elementu są kontrolowane przez cztery podstawowe właściwości przestrzene:

- **Szerokość Wykreska Ograniczającego (BBox):** Fizyczna szerokość konturów znaku, mierzona od lewego punktu konturu (lewego krawędzi wykresu) do prawego punktu (prawa krawędzi wykresu).
- **Odległość od lewej strony (LSB):** Odległość między początkiem znaku (punktem zero na osi poziomej) a lewą krawędzią wykresu ograniczającego. Reprezentuje negatywną lub dodatwną przestrzeń białą po lewej stronie znaku.
- **Odległość od prawej strony (RSB):** Odległość między prawej krawędzią wykresu ograniczającego a granicą szerokości postępu.
- **Szerokość postępu:** Całkowita przestrzeń pozioma przydzielona znaku. Ta wartość określa odległość poziomą, którą kursor tekstu przesuwa po wpisaniu znaku. Jest sumą LSB, szerokości wykresu ograniczającego i RSB.

> [!UWAGA] Odległości od strony mogą być dodatnie (dla typowego rozmieszczenia) lub ujemne (gdy części konturu, takie jak serwety „T” czy „f”, przekraczają granicę szerokości postępu).

## Narzędzie Metryk i Pasek Właściwości

Aby edytować te wartości, aktywuj narzędzie **Metryk** klikając jego ikonę w Pasku Narzędzi lub naciskając `M`. Jeśli nie jest otwarte okno Znaku, aktywowanie narzędzia automatycznie otworzy jedno dla wybranego znaku.W trybie Metrics aktywny glyph jest wyróżniony kontrastującymi liniami sidebearingu. Jeśli linie te są ukryte, kliknij przycisk **Show Spacing Controls** w pasku właściwości. Pasek właściwości Metrics wyświetla edytowalne pola dla **L** (LSB), **R** (RSB) i **W** (Szerokość).

Twórcy mogą edytować rozmieszczenie w trzech sposobach:

1. Przesuwanie linii sidebearingu lub przycisków trójkątnych bezpośrednio w okienku Glyph.
2. Kliknięcie i przesunięcie samego glypha w celu ponownego rozmieszczenia LSB i RSB bez zmiany całkowitej szerokości postępu (lub przesuwanie Alt w celu dostosowania szerokości postępu).
3. Wstawianie wartości bezpośrednio w pola pasku właściwości, w Tabeli Metriców lub w panelu Glyph.

> [!TIP] Naciskanie klawisza semicolonu (`;`) w trybie Metrics uruchamia algorytm automatycznego rozmieszczenia FontLab, który natychmiast przypisuje sidebearing optyczny obecnemu glyphowi.

## Związanie sidebearingu i łukowego italicu

FontLab 7 pozwala projektantom na łączenie metryk za pomocą **związanych wyrażeń metryk**. Zamiast numeryrów manualnych, można wpisać nazwę glypha (np. `o` lub `H`) w pola LSB, RSB lub Szerokość. FontLab obsługuje podstawowe operacje matematyczne (np. `o * 1.05 + 10`).To połączenie metryk w różnych masterach, użyj prefiksu koloń (np. `:Regular` lub `:Regular * 1.1`). Dla automatycznych aktualizacji włącz **Font > Live Update > Live Metrics**.

Dla fontów italskich, boczne odległości muszą być mierzone wzdłuż ukośności. Włącz **View > Apply Italic Angle to Metrics** (lub włącz **Preferences > Grid > Follow the font’s Italic Angle**) aby przekrzywić sieć metryk. To zapewnia, że współrzędne LSB i RSB są obliczane równolegle do osi italskiej, utrzymując spójność wizualną w projektach ukośnych.

---

# Rozdział 15: Klasy i wyjątki kerningu

Kerning dostosowuje poziom przestrzeni poziomej między konkretnymi parymi glyphami, aby osiągnąć spójną wizualną odległość, uzupełniając domyślne boczne odległości. Chociaż kerning płaski (glyph do glypha) jest prosty, może znacznie powiększać pliki fontów. Aby optymalizować tabele GPOS, FontLab 7 wykorzystuje kerning oparty na klasach OpenType.

## Klasy kerningu lewego vs. prawego

Aby efektywnie zarządzać kerningiem, glyphy o podobnych kształtach optycznych są grupowane w klasy kerningu. Ponieważ glyph wykazuje różne zachowanie w zależności od tego, czy pojawia się po lewej czy po prawej stronie pary, FontLab 7 rozróżnia:

- **1. klasa kerning (lewa strona):** Stosowana, gdy glyph znajduje się po lewej stronie pary. Na przykład glyphy takie jak `O`, `Q` i `C` mają wspólny wskaźnik klasy dla swoich prawych wysunięć.
- **2. klasa kerning (prawa strona):** Stosowana, gdy glyph znajduje się po prawej stronie pary. Na przykład glyphy takie jak `O`, `U` i `D` mają wspólny wskaźnik klasy dla swoich lewych wysunięć.

Glyph może należeć do jednej klasy 1. i jednej klasy 2. W obrębie każdej klasy określony **kluczowy glyph** (lub lider klasy) definiuje relację odległości dla całej grupy.

> [!WAŻNE] Glyph nie może należeć do wielu klas na tej samej stronie. Takie zachowanie powoduje konflikty, które uniemożliwia kompilację tabeli GPOS.

## Workflow i wyjątki w kerningu klasy

Aby stworzyć workflow kerningu klasy, projektanci grupują glyphy pod klasy lewe i prawe oraz definiują kerning dla liderów klasy. W workflowzie klasa do klasy, dostosowanie odległości między dwoma kluczowymi glyphami automatycznie stosuje to dostosowanie do wszystkich kombinacji glyphów w tych klasach. To znacznie zmniejsza koszt definiowania korekt parzystych dla każdej kombinacji.Jednak niektóre pary wymagają unikalnego rozmieszczenia znaków, które odbiega od reguły klasy. Są one obsługiwane jako **wyjątki w kerningu**:

1. Wybierz parę w Okienku Glyph z aktywnym narzędziem **Kerning** (`K`).
2. Znajdź ikony blokad w barce Właściwości lub panelu Kerning obok aktywnych znaków.
3. Kliknij ikonę blokady, aby ją odblokować i oddzielić znak od jego klasy dla tej pary.
4. Dostosuj wartość kerningu, aby napisać wyjątek specyficzny dla znaku, które przekracza regułę klasy.

> [!TIP] Miej wyjątki jak najmniej. Nadmierne wyjątki powiększają rozmiary tabeli GPOS i mogą powodować problemy z renderowaniem w środowiskach starszych.

## Panel Pary i Wyrażeń

Systematyczne testowanie jest kluczowe dla wysokiej jakości kerningu. Użyj panelu **Pary i Wyrażeń** (`Window > Panels > Pairs & Phrases`) do weryfikacji kombinacji:

- **Selekcja listy:** Zainstaluj zdefiniowane listy powszechnych par, słów lub tekstu dostosowanych.
- **Filtrowanie:** Filtruj listę, aby wyświetlić tylko aktywne pary, pary klasyczne lub konkretne znaki.
- **Nawigacja:** Kliknij dwa razy na jakąkolwiek parę w panelu, aby natychmiast ją wyświetlić w Okienku Glyph dla szybkiego edytowania.

## Szybkie kontrolki i edycja kerninguGdy narzędzie Kerning jest aktywne, można edytować wartości kerning w sposób wizualny lub numeryczny:

- **Przesuwanie wizualne:** Przesuń aktywny glyph lub interaktywny przycisk kerning między glyphami, aby dostosować odległość.
- **Skróty klawiszowe:** Naciśnij klawisze strzałek „Left”/`Right” dla dostosowań o wielkości 1 jednostki, lub trzymaj `Shift”, aby wykonywać kroki o wielkości 10 jednostek.
- **Barwa właściwości:** Wstaw precyzyjne wartości numeryczne bezpośrednio do pola kerningu znajdującego się na górze okna.

---

# Rozdział 16: Funkcje układu tekstu OpenType

Funkcje układu tekstu OpenType przekształcają statyczne glyphy w dynamicne, inteligentne systemy typograficzne. Definiując substytucje glyphów i precyzyjne dostosowania pozycji, projektanci mogą zarządzać złożonymi pismami, ligaturami, małymi literami, alternatywnymi wariantami kontekstowymi oraz przyłączeniami mark-to-base. FontLab 7 zapewnia kompleksne środowisko do pisania, kompilowania, testowania i zarządzania tym kodem układu tekstu przy użyciu standardowej składni Adobe Feature File (FEA).

## Panel funkcji

Centralnym centrum do zarządzania kodem funkcji jest **Panel funkcji** (Window > Panels > Features). Tutaj można definiować klasy glyphów, bloki prefiksów i konkretne funkcje OpenType (takie jak `liga`, `smcp` czy `kern`).- **Klasy Glyfów**: Grupa glyfów dzielonych na zasadnicze role typograficzne (np. litery małe, małe kapsy lub podstawowe glyfy), aby uprościć zasady. FontLab obsługuje zarówno klasy nazwane (np. `@lc_vowels`), jak i klasy wstawione.
- **Przedrostek**: Dodawanie deklaracji globalnych, takich jak deklaracje languagesystem (np. `languagesystem latn dflt;`), które rejestrują funkcje w różnych systemach operacyjnych, silnikach układu i aplikacjach.
- **Funkcje**: Pojedyncze bloki zawierające zasady substitucji i pozycjonowania, grupowane według czteroliterowych tagów OpenType.

> [!TIP] Można automatycznie generować standardowe funkcje, wybierając **Create Features from Font Info** w menu panelu. FontLab analizuje nazwy glyfów, aby generować zasady dla ligatury, małych kaps i figur.

## Tworzenie Zasad Substitucji i Pozycjonowania

Kod funkcji OpenType dzieli instrukcje na dwie główne kategorie: GSUB (Substitucja Glyfów) i GPOS (Pozycjonowanie Glyfów).

### Substitucje Glyfów (GSUB)

Substitucje zastępują jeden lub więcej glyfów alternatywnymi glyfami. Najczęstsze zasady substitucji obejmują:

- **Ligatury (`liga`, `dlig`)**: Wiele wprowadzanych znaków zastępuje pojedynczy znak kompozytowy. `sub f i by f_i;`
- **Małe wielkie kropki (`smcp`, `c2sc`)**: Zastępuje standardowe małe lub duże litery z wariantami małych wielkich kropki. `sub a by a.sc;`
- **Alternatywy kontekstowe (`calt`)**: Zastępuje znak w zależności od otaczającego go kontekstu znaków. `sub f' [i e] by f.short;`

### Pozycjonowanie znaków (GPOS)

Zasady pozycjonowania dostosowują umieszczenie lub szerokość naprzód znaków bez ich zastępowania. Jest to kluczowe dla kerningu i umieszczenia diakrytycznych znaków:

- **Dostosowanie par (Kerning)**: Przesuwa odległość między konkretnymi parami znaków. `pos T e -50;`
- **Przyczepienie znaku (mark, `mkmk`)**: Przyczepia diakrytyczne znaki do znaków podstawowych za pomocą punktów przyczepienia opartego na współrzędnych. `pos base [a] <anchor 450 600> mark @TOP_MARKS;`

> [!WAŻNE] Podczas definiowania dostosowań pozycjonowania, FontLab bezpośrednio tłumaczy wizualne punkty przyczepienia (takie jak `top` lub `bottom` definiowane wewnątrz okna znaków) na kod przyczepienia GPOS podczas kompilacji.

## Kompilacja i testowanie funkcjiCechy OpenType muszą być skompilowane do tabel binaryowych, aby funkcjonować. FontLab 7 używa zintegrowanej biblioteki Adobe AFDKO do kompilacji kodu funkcji w aplikacji.

- Aby kompilować, kliknij przycisk **Compile** (ikonka gry) w panelu Features. Wszystkie błędy składniowe lub ostrzeżenia kompilacji pojawią się w panelu Output.
- Aby sprawdzić kompilowane funkcje, otwórz panel **Preview** (Window > Panels > Preview). Wpisz stringy testowe i przełącz aktywne funkcje z wyboru funkcji panelu, aby sprawdzić subskrypcje i umieszczenie w czasie rzeczywistym.

## Zarządzanie zewnętrznymi plikami funkcji

Dla złożonych prac FontLab umożliwia ładowanie i zapisywanie zewnętrznych plików `.fea`. Poprzez menu panelu Features możesz importować zewnętrzny kod funkcji, aby zastąpić lub dodać do istniejących reguł.

> [!NOTE] Importy zewnętrznych FEA są analizowane i mapowane do istniejących glyphów. Upewnij się, że wszystkie nazwy glyphów w plikach zewnętrznych dokładnie odpowiadają nazwom glyphów w FontMapie FontLab.

---

# Rozdział 17: Informacje o fontie i konfiguracja osiPanel **Font Info** (File > Font Info) służy jako centralny repozytor wszystkich metadanych, atrybutów stylistycznych, wskaźników globalnych i parametrów zmienności w projekcie FontLab. Dokładne konfigurowanie tych ustawień jest kluczowe dla generowania pełnie funkcjonalnych fontów OpenType, TrueType i Variable.

## Struktura metadanych Font Info

Font Info jest organizowany w hierarchiczne sekcje. Podstawowe metadane obejmują:- **Nazwy**: Zawiera pola nazewnictwa wymagane na różnych systemach operacyjnych.
- **Strategie nazewnictwa rodzin**: FontLab zarządza złożoną strukturą nazewnictwa wymaganą przez platformy tradycyjne i nowoczesne. Nazwa rodzina służy jako identyfikator główny, natomiast nazwy stylów rozróżniają warianty. Najlepsza praktyka polega na konfigurowaniu zarówno _Preferowanej Rodziny_ (z dopuszczeniem nieograniczonej liczby wag i stylów), jak i _Rodziny Mapy Stylu_ (ograniczające grupy stylów do standardowej czterostylistycznej struktury RIBBI: Regularny, Italski, Klasowy, Klasowy Italski) dla maksymalnej kompatybilności.
- **Stylizacja i klasyfikacja**: W zakresie _Klasyfikacji_ użytkownicy mogą określić klasę wagi, klasę szerokości i nachylenie każdego mastera. Dodatkowo, parametry **PANOSE** pozwalają na określenie numerycznych opisów charakterystyk takich jak styl serif, proporcje, kontrast i zachowanie w linii środkowej. Te wartości pomagają systemom operacyjnym w zastąpieniu brakujących fontów wyglądającymi podobnie.
- **Metrici i parametry**: Globalne metrici – w tym ascender, descender, wysokość kapitału, x-height i strefy alinyzacji – są definiowane dla każdego mastera. Te wartości decydują o metricach pionowych i wpływają na zachowanie automatycznego wskazywania.> [!IMPORTANT] Niespójne nazewnictwo rodziny pism lub błędnie skonfigurowany mapowanie stylu RIBBI może prowadzić do konfliktów instalacyjnych, błędów w łączeniu stylu między platformami oraz nieprawidłowego wyświetlania w programach do przetwarzania tekstu.

## Ustawienie osi zmienności

Podczas projektowania fontu zmiennego lub rodziny pism wielomasterowej, definiowanie osi przestrzeni projektowej jest głównym krokiem. Oś reprezentuje kierunek zmienności, takie jak Waga, Szerokość lub osobne osie projektowe.

- **Osy standardowe**: Zwykle używa się standardowych czteroliterowych tagów definiowanych przez specyfikację OpenType, takich jak `wght` (Waga) i `wdth` (Szerokość).
- **Osy specjalne**: Można utworzyć osoby specjalne używając tagów wielkich liter (np. `GRAD` dla Grade, `SERF` dla Serif Size).

Każda oś wymaga tagu, nazwy i zdefiniowanego zakresu. Każdy master znajduje się w specyficznym punkcie koordynacyjnym.

> [!NOTE] Każdy master glyph musi mieć dokładnie tę samą liczbę konturów, węzłów, obszarów i punktów początkowych, aby zapewnić kompatybilność interpolacji. Zmiana ciągłości węzłów (np. ciągłości krzywizny G2) lub zmiana kierunku konturów między masterami spowoduje awarię interpolacji.

## Mapowanie osi w grafieJedną z najpotężniejszych funkcji w silniku wariacji FontLab 7 jest **Axis Graph**, który mapuje współrzędne przestrzeni projektowej do współrzędnych użytkownika.

1. **Współrzędne przestrzeni projektowej**: Czyste, wewnętrzne wartości używane podczas rysowania (np. pomiary grubości trzonka w wielkościach od 40 do 180 jednostek, które bezpośrednio wpływają na umieszczenie węzłów krzywizny Bezier i szerokość postępu).
2. **Współrzędne użytkownika**: Zewnętrzne wartości udostępniane użytkownikom końcowym (np. skala wagi CSS od 100 do 900).

Axis Graph definiuje mapowanie między tymi dwoma przestrzeniami. Domyślnie to mapowanie jest liniowe. Jednak progresja wag wizualnych rzadko jest liniowa; skok z Light (300) do Regular (400) wymaga innego fizycznego wzrostu szerokości trzonka i bocznych elementów niż skok z Bold (700) do Black (900).

> [!TIP] Użyj Axis Graph do stworzenia nieliniowego mapowania. Zapewnia to gładkie interpolacje przy skalowaniu i wizualnie zrównoważone przejścia, nawet jeśli podstawowe przesunięcia współrzędnych krzywizny Bezier są nieliniowe.

---

# Rozdział 18: Fonty zmiennych i kompatybilność z konturamiW FontLab 7 proces pracowania z wieloma głównymi wzorami i osiami projektowymi w celu wygenerowania dynamicznych instancji nazywany jest zmiennością. Tworzenie fontu zmiennego wymaga utworzenia przestrzeni projektowej i zapewnienia, aby kontury głównych wzorów były w pełni kompatybilne dla interpolacji.

## Projektowanie przestrzeni projektowej

Przestrzeń projektowa jest definiowana przez jedną lub więcej osi zmienności – takich jak Weight (`wght`), Width (`wdth`) czy Slant (`slnt`) – skonfigurowanych w **Font Info > Axes**. Główne wzory fontów i wzory bez fontów (definiowane na poziomie glyphów za pomocą nazw z sufiksem lokalizacji osi, takich jak `:wt=350,wd=75`) są mapowane do konkretnych współrzędnych w tej wielowymiarowej przestrzeni projektowej. FontLab 7 używa tych współrzędnych do obliczania interpolacji i ekstrapolacji pośrednich instancji.

> [!IMPORTANT] Upewnij się, że wszystkie style głównych wzorów mają unikalne położenie w przestrzeni projektowej. Nie będziesz mógł poprawnie eksportować swojego fontu ani przeglądać zmienności, jeśli dwa główne wzory mają identyczne współrzędne.

## Zasady kompatybilności konturów

Dla gładkiej interpolacji geometria konturów każdego glypha musi idealnie zgadzać się we wszystkich aktywnych głównych wzorach. Kontury są kompatybilne, gdy spełniają następujące wymagania strukturalne:1. **Liczba dopasowań**: Glyph musi mieć tę samą liczbę elementów i konturów, a każdy kontur musi zawierać dokładnie tę samą liczbę węzłów (zarówno ostrych, jak i gładkich) oraz punktów kontrolnych krzywych Bézier.
2. **Dopasowanie punktów początkowych**: Wyznaczony punkt początkowy (indeks węzła 0) każdego konturu musi znajdować się w tej samej względnej pozycji topologicznej we wszystkich masterach. Jeśli punkty początkowe nie są dopasowane, kontur będzie się kręcił lub sam siebie przecinał podczas interpolacji.
3. **Spójny kierunek konturów**: Kontury muszą przepływać w tym samym kierunku (albo w kierunku wskazówek zegara dla liczników, albo przeciwnie dla ścieżek zewnętrznych) we wszystkich masterach. Niespójny kierunek powoduje artefakty wyświetlania i wypełniania.

> [!TIP] Włącz **Edit > Match when Editing**, aby synchronizować dodawanie, usuwanie i korekty węzłów we wszystkich kompatybilnych masterach jednocześnie, zachowując kompatybilność konturów podczas procesu rysowania.

## Diagnoza i rozwiązywanie niespójności

FontLab 7 zapewnia kilka specjalistycznych interfejsów do weryfikacji kompatybilności konturów przed eksportem:- **Filtr Sidebaru Non-Matching**: W okienku Font rozszerzcie sekcję **Layers & Masters** w sidebarze. Filtr **Non-matching** wyświetla dokładną liczbę niezgodnych glyphów. Kliknięcie na ten filtr izoluje te glyphy w celu szybkiego rozwiązania problemów.
- **Narzędzie Matchmaker**: Aktywuj to narzędzie naciskając klawisz `7`. W pasku właściwości wyświetla się zielony wskaźnik statusu, jeśli masters są kompatybilne, a czerwony, jeśli nie. Narzędzie Matchmaker pokazuje numery węzłów i kody kolorów odpowiadających konturom. Można wybrać odpowiadające sobie zakresy węzłów i pozwolić narzędziu Matchmakerowi automatycznie zharmonizować segmenty ścieżki.
- **Przybliżenie Interpolation**: Użyj panelu **Variations**, aby nawigować w przestrzeni projektu. Rysując wektor interpolacji w widoku Map, można sprawdzić **Interpolation** w panelu Preview, aby przejrzeć etapy pośrednie.

## Eksport Fontu Zmiennych

Po potwierdzeniu kompatybilności wybierz **File > Export Font As** i wybierz format zmienny, np. **Variable TT (.ttf)** lub **Variable PS (.otf)**. FontLab kompiluje parametry przestrzeni projektu, domyślne struktury masters i delty interpolacji do ostatecznego fontu OpenType Variations.# Rozdział 19: Skryptowanie i Automatyzacja w Pythonie

FontLab 7 zawiera wbudowany, cross-platformowy środowisko skryptowania Pythona 3, które umożliwia projektantom czcionek i inżynierom fontów automatyzowanie powtarzalnych zadań, wykonywanie modyfikacji w batchu oraz rozszerzanie interfejsu aplikacji. Poprzez interakcję z wewnętrznymi strukturami danych FontLab, skrypty mogą programowo manipulować krzywymi Bezier, dostosowywać poziome sidebearings i szerokości, zarządzać funkcjami układu OpenType oraz tworzyć własne procesy pracy.

## Panel i środowisko Skryptowania

Głównym interfejsem do wykonywania kodu skryptowego jest **Panel Skryptowania** (_Window > Panels > Scripting_). Panel zawiera prosty edytor kodu z podświetlaniem składni, konsolę wyjściową wyświetlającą wyniki lub błędy wykonania, oraz kontrolki do uruchamiania skryptów. Użytkownicy mogą pisać kod bezpośrednio w edytorze, ładować zewnętrzne skrypty `.py` lub uruchamiać pojedyncze instrukcje interaktywnie.

Dodatkowo, skrypty zapisane w folderze `Scripts` użytkownika są automatycznie rejestrowane w menu _Tools > Scripts_, co umożliwia przypisanie im własnych skrótów klawiszowych.

## API wysokiego poziomu `fontlab`

## `fontlab` API wysokiego poziomuPakiety `fontlab` to nowoczesny, wysokiego poziomowy API Pythona zaprojektowany do intuicyjnego edycji znaków i glyphów. Służy jako oplot dla aktywnego miejsca pracy, zapewniając obiekty wysokiego poziomu do zapytania i modyfikacji obecnego stanu projektu:

- **Aktywne Miejsce Pracy:** Klasa `flWorkspace` zarządza zarządzaniem poziomem okna. Dostęp do aktywnego miejsca pracy uzyskuje się za pomocą `fontlab.flWorkspace()`.
- **Obecny Znak (Pakiety):** Funkcja `CurrentFont()` zwraca aktywny znak jako obiekt `flPackage`. Poprzez ten obiekt można uzyskać dostęp do globalnych właściwości znaków, masters, metadanych informacji o znakach, klasy oraz zbioru glyphów znaków.
- **Wybrane Glyphy:** Funkcja `CurrentGlyph()` zwraca obiekt `flGlyph` aktywny, który aktualnie jest otwarty w Okienku Glyphów, natomiast `CurrentFont().selectedGlyphs` zwraca listę wszystkich wybranych glyphów w Okienku Znaków. Można programowo iterować przez te glyphy, aby modyfikować węzły konturu, przesuwać sidebearings lub dodawać anchory.

> [!TIP] Podczas programowej modyfikacji konturów glyphów, należy używać współrzędnych typu floating-point, aby zachować precyzję krzywy Bezier i ciągłość węzłów G2 między masters. Liczby całkowite należy używać tylko przed finalnym eksportem znaków.## APIy niskiego poziomu i starszych wersji: `fontgate` i `FL`

Dla głębokiej kontroli nad podstawowym silnikiem aplikacji i kompatybilności z starszymi skryptami, FontLab 7 udostępnia dwa dodatkowe pakiety:

- **Pakiet `fontgate`:** Ten niskiego poziomu, wypełniony C++ biblioteka zawiera surowe struktury danych podstawowego silnika FontLab. Obsługuje podstawowe klasy geometryczne i seryalizacji, takie jak `fgFont`, `fgGlyph`, `fgContour` i `fgPoint`. Chociaż jest trudniejszy w napisaniu, zapewnia wysokiej wydajności przetwarzanie przy wykonywaniu intensywnych operacji na tysiącach węzłów lub współrzędnych.
- **Pakiet `FL`:** Aby zapewnić kompatybilność z przeszłością, FontLab 7 zawiera starszy API `FL`. Simuluje interfejs skryptowy Python 2 w FontLab Studio 5. Używanie `FL` pozwala programistom uruchamiać starsze skrypty z minimalnymi zmianami, ułatwiając przejście na nowoczesny API Python 3.

## Customne interfejsy użytkowników z PythonQt

Poprzez integrację **PythonQt**, skrypty mogą uzyskać dostęp do podstawowego frameworku Qt, aby tworzyć bogate, native interfejsy użytkownika.Zamiast działać cicho lub polegać na prostych komendach w linii komend, programiści mogą importować moduły z `PythonQt.QtGui` i `PythonQt.QtCore`, aby tworzyć własne dialogi, pola wprowadzania tekstu, przyciski i panely ustawień. Te własne okna dziedziczą stylistykę FontLab i funkcjonują w głównym pętli aplikacji.

> [!IMPORTANT] Podczas tworzenia własnych okien UI za pomocą PythonQt, zawsze upewnij się, że twoje dialogi są prawidłowo powiązane z głównym oknem FontLab, aby uniknąć problemów z blokowaniem uwagi lub awarii aplikacji przy zakończeniu skryptu.

---

# Rozdział 20: Testowanie, Weryfikacja i Eksportowanie

Przed udostępnieniem fontu niezbędny jest systematyczny proces kontroli jakości, inspekcji szkicu i weryfikacji kompilacji. FontLab 7 zapewnia wbudowane narzędzia do przeglądu zachowania układu, diagnozy błędów konturów, konfigurowania profili eksportu technicznego i pakowania finalnych fontów statycznych lub zmiennych.

## Kontrola Jakości i Weryfikacja WizualnaTestowanie wizualne rozpoczyna się w panelu **Preview**, który jest żywym sandboxem do renderowania, rozmieszczenia i funkcji OpenType. W przeciwieństwie do standardowego okna Glyph, panel Preview pozwala na wpisywanie specjalnych ciągów tekstu, testowanie kroków interpolacji w ramach masters i sprawdzanie zachowań renderowania w różnych rozmiarach. Można wybrać różne tryby (np. Content, Spacing lub Kerning) i przejrzeć pojedyncze masters lub konkretne miejsca w przestrzeni projektowej.

Aby sprawdzić funkcje układu tekstu – takie jak ligatury (`liga`), małe kapsy (`smcp`) czy umieszczenie znaków na podstawie (`mark`) – należy najpierw skompilować kod funkcji OpenType. Otwórz panel **Features** i kliknij przycisk **Compile**. Po skompilowaniu funkcje te mogą być włączone lub wyłączone bezpośrednio w panelu Preview lub w narzędziu tekstowym, aby upewnić się, że zasady substitucji i umieszczania działają zgodnie z planem.

> [!NOTE] Jeśli Twoja rodzina fontów zawiera wiele masters, a zdefiniowałeś funkcje ręcznie, upewnij się, że profile eksportu są skonfigurowane tak, aby tworzyć funkcje dla każdego master oddzielnie. To zapobiega duplikacjom definicji funkcji, które mogą zastępować unikalne metryki masters.

## Automatyczne audyty z FontAuditFontLab’s **FontAudit** to automatyczny silnik, który analizuje kontury znaków w celu wykrycia błędów technicznych. Można go aktywować za pomocą `View > Show > FontAudit` lub otworzyć panel FontAudit (`Window > Panels > FontAudit`) aby sprawdzić aktualny warstwę. Aby audytować kilka znaków, wybierz je w okienku Font i wybierz `Glyph > FontAudit Glyphs`. Czerwone flagi wskazują na rozwiązane i nierozwiązane problemy, które można naprawić globalnie za pomocą `Glyph > Fix FontAudit Problems` lub indywidualnie w panelu. Kluczowe sprawdziany obejmują:

- **Przecięcia:** Przekrywające się kontury, które mogą powodować artefakty rasterizacji.
- **Brak ekstremów:** Segmenty krzywej, które nie mają węzłów w najbardziej zewnętrznych punktach pionowych lub poziomych. Węzły ekstremów są kluczowe dla umieszczenia wskazówek i spójności interpolacji.
- **Płaskie krzywe:** Segmenty krzywej Bezier z równo ustawionymi uchwytami, które można bez straty uproszczyć na linie prostą.
- **Nieregularne i rzadkie trzonki:** Niespójności w grubości trzonków w porównaniu z powszechnie ustawionymi wartościami w `Font Info > Stems`.

## Ustawienie profilu eksportuEksportowanie przekształca pliki źródłowe rozwoju (`.vfc`/`.vfj`) w formaty gotowe do produkcji za pomocą dialogu **Export Profiles** (`File > Export Profiles...`). Profile określają, jak FontLab przetwarza kontury, obsługuje nazwy glyphów i kompiluje tabele OpenType w wyniku eksportu.

Można dostosować profile, aby kontrolować precyzję współrzędnych. TrueType outlines (`.ttf`) wymagają zaokrąglenia współrzędnych do liczb całkowitych, natomiast PostScript outlines (`.otf`) obsługują współrzędne dzielące, aby zachować dokładność krzywych Bezier przy mniejszym rozmiarze pliku. Profile również zarządzają tym, czy usunąć krawędzie z pętlą, czy przekształcić nazwy glyphów rozwojowych w nazwy produkcyjne oraz generować funkcje OpenType kerning lub mark-to-mark (`mkmk`).

## Kompilowanie i Pakowanie

Aby generować twoje ostateczne fonty, wybierz `File > Export Font As...`.

- **Static OTF/TTF:** Wybierz standardowe profile OpenType PS (`.otf`) lub OpenType TT (`.ttf`).
- **Variable Fonts:** Użyj profilu **Variable TT (.ttf)**. W przypadku pakowania zmiennych wszystkie masters muszą zachować kompatybilność węzłów – co oznacza identyczne kierunki konturów, odpowiednie liczby węzłów i identyczne punkty początkowe.