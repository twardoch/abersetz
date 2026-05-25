# FontLab 7: Pełny przegląd 20 rozdziałów

Ten dokument zawiera połączony, 20-rozdziałowy szczegółowy przegląd możliwości, narzędzi i przepływów pracy FontLab 7.

---

# Rozdział 1: Witamy w FontLab 7

## Wprowadzenie i wymagania systemowe

FontLab 7 to wszechstronny, profesjonalny edytor czcionek na komputery stacjonarne, zaprojektowany tak, aby spełniać rygorystyczne wymagania projektantów czcionek, typografów i inżynierów czcionek. Zbudowany na całkowicie przepisanym silniku w porównaniu do starszych platform, takich jak FontLab Studio 5, FontLab 7 oferuje nowoczesny, nieniszczący proces edycji. Działa natywnie na systemie macOS 10.10 (Yosemite) i nowszych, a także Windows 7 i nowszych. Aplikacja obsługuje wyświetlacze o wysokiej rozdzielczości i bezproblemowo integruje się z rurociągami produkcyjnymi. W przeciwieństwie do swojego poprzednika, który opierał się na oddzielnych plikach dla różnych formatów, FontLab 7 wprowadza ujednolicony format roboczy `.vfc` (Dokument FontLab), który przechowuje wszystkie warstwy glifów, odniesienia i osie zmiennych w jednym pliku bazy danych.> [!UWAGA] Dla nowych użytkowników oceniających oprogramowanie FontLab 7 oferuje w pełni funkcjonalną 30-dniową wersję próbną. W okresie próbnym wszystkie profesjonalne narzędzia — w tym generowanie czcionek, kompilowanie funkcji OpenType i skrypty w języku Python — pozostają w pełni aktywne bez znaków wodnych i ograniczeń projektowych.

## Pozycja w branży i możliwości

Jako standard w branży czcionek cyfrowych, FontLab 7 jest używany przez największe wytwórnie czcionek i niezależnych projektantów do opracowywania wszystkiego, od wyświetlaczy o pojedynczej gramaturze po masywne, wieloosiowe rodziny czcionek zmiennych. Edytor zapewnia niezrównane narzędzia do rysowania zoptymalizowane pod kątem precyzyjnego projektowania wektorów. Projektanci mogą manipulować krzywymi Béziera za pomocą zaawansowanej kontroli ciągłości węzłów (w tym dopasowywania krzywizny G2), przesuwać punkty wzdłuż konturów bez zmiany geometrii krzywej oraz równoważyć uchwyty, aby zapewnić optymalną jakość konturu. Środowisko rysunkowe obsługuje zarówno krzywe PostScript (sześcienne Béziera), jak i TrueType (kwadratowe Béziera), umożliwiając programistom bezstratną konwersję pomiędzy typami krzywych.FontLab 7 oferuje natywną obsługę wielu skryptów. Zawiera kompleksowe narzędzia do systemów projektowania obejmujących zestawy znaków łacińskich, cyrylicy, greckich, arabskich, hebrajskich, indyjskich oraz chińskich, japońskich i koreańskich (CJK). Poza tradycyjnymi formatami FontLab 7 jest liderem nowoczesnych technologii czcionek, oferującym solidne możliwości w zakresie:

- **Czcionki zmienne (odmiany czcionek OpenType):** Bezpośrednia edycja osi przestrzeni projektowej, wzorców i zgodności interpolacji, z wizualnymi wskaźnikami dopasowania konturów.
- **Czcionki kolorowe:** Obsługa formatów map bitowych OpenType-SVG, COLR/CPAL i CBDT/CBLC.
- **Inteligentna interpolacja:** Precyzyjne zarządzanie projektami głównymi, metrykami i klasami kerningu w przestrzeniach wielowymiarowych.

## Metryki i mechanika projektowaniaProjektowanie wysokiej jakości krojów pisma wymaga szczególnej dbałości o odstępy. FontLab 7 obsługuje łożyska boczne, szerokości postępów i kerning z zaawansowaną matematyczną precyzją. Użytkownicy mogą dynamicznie łączyć metryki za pomocą formuł, zapewniając, że zmiany w konturze glifu natychmiast aktualizują jego relacje między odstępami. Zintegrowane narzędzia Metrics i Kerning działają w środowisku edytora tekstu, ułatwiając sprawdzanie w czasie rzeczywistym złożonych kombinacji skryptów. Umożliwia to projektantom typów dostosowywanie łożysk bocznych i par kerningu bezpośrednio w kontekście, wykorzystując kerning oparty na klasach do wydajnego zarządzania tysiącami par.

## Ewolucja i ciągłe aktualizacje

W przeciwieństwie do statycznych cyklów rozwoju starszych narzędzi, FontLab 7 jest narzędziem stale rozwijającym się. Znaczące ulepszenia, nowe polecenia, optymalizacje wydajności i udoskonalenia przepływu pracy zostały wprowadzone w mniejszych wersjach (np. 7.1, 7.2 i kolejnych wydaniach dot).

> [!WAŻNE] Aby zachować zgodność z rozwijającymi się systemami operacyjnymi i specyfikacjami czcionek, użytkownicy muszą regularnie przeglądać uwagi do wersji pomocniczej. Notatki te służą jako podstawowa dokumentacja nowych funkcji i zmienionych skrótów klawiaturowych.

---# Rozdział 2: Projektowanie i dostosowywanie interfejsu użytkownika

## Paradygmaty układu przestrzeni roboczej

FontLab 7 posiada wysoce elastyczny interfejs użytkownika, zaprojektowany tak, aby dostosować się do różnych stylów projektowania i konfiguracji z wieloma monitorami. W **Preferencje > Ogólne** możesz skonfigurować interfejs tak, aby działał w jednym z trzech trybów okna:

- **Tryb pojedynczego okna/kart:** Dokumenty, okna czcionek i okna glifów są zorganizowane jako zakładki w jednej głównej ramce aplikacji. Dzięki temu przestrzeń robocza pozostaje czysta, a okna nie zachodzą na siebie.
- **Tryb pływającego systemu Windows:** Każdy otwarty obszar roboczy czcionek i glifów istnieje w niezależnym, pływającym oknie. Jest to idealne rozwiązanie w przypadku konfiguracji z wieloma monitorami, umożliwiając przeciąganie rysunków, edytorów metryk i okien podglądu między ekranami.
- **Zakładki Okna i Okna:** Podejście hybrydowe umożliwiające dokowanie okien razem lub przemieszczanie się. Aby zadokować pływające okno, użyj opcji **Okno > Dokowanie > Okno można dokować** lub połącz je za pomocą poleceń takich jak **Scal wszystkie okna** lub **Scal z czcionką Windows**.

## Dokowanie i grupowanie paneliPanele w FontLab 7 są bogate w kontekst i mogą swobodnie się przemieszczać lub zaczepiać do krawędzi ekranu, okna aplikacji lub innych paneli. Aby zadokować panel, przeciągnij jego pasek tytułu w stronę krawędzi innego panelu lub okna. Jasnoniebieska linia wskazuje prawidłową strefę dokowania, a podczas przeciągania panel staje się półprzezroczysty. Aby utworzyć grupę paneli z zakładkami, przeciągnij panel bezpośrednio nad inny panel. Panel odbiorczy jest podświetlony na niebiesko; upuszczenie panelu łączy je, wyświetlając ich tytuły na dole grupy.

> [!UWAGA] Kiedy panel jest ruchomy, kwadratowy przełącznik w prawym górnym rogu określa jego zachowanie podczas dokowania:
>
> - **ڰ (Plus):** Można dokować przy krawędziach ekranu lub pomiędzy panelami, można je grupować, ale nie można dokować wewnątrz okna.
> - **ڰ (Odwrócona L):** Zachowanie domyślne. Panel można zadokować do dowolnego okna lub obramowania panelu, krawędzi ekranu lub grupy z innymi.
> - **ڰ (Pusty):** Panel jest zablokowany w stanie ruchomym i nie można go zadokować ani grupować.

## Pasek właściwości kontekstowych

Pasek właściwości znajduje się w górnej części okien czcionek i glifów, zapewniając natychmiastowy dostęp do ustawień.- **Okno czcionek (statyczne):** Pasek właściwości pozostaje stały. Zawiera przełączniki paska bocznego („◧”), tabeli („▦”) i listy („◨”), a także opcje podpisów komórek, filtry potencjalne (kodowanie, kategoria, skrypt), selektory sortowania, podświetlanie flag/znaków i pole wyszukiwania.
- **Okno glifów (dynamiczne):** Środkowa część paska dostosowuje się do aktywnego narzędzia (takiego jak Kontur, Powiększenie, Prowadnice, Metryki lub Kerning) lub bieżącego zaznaczenia. Lewa i prawa sekcja pozostają statyczne, pokazując przełączniki paska bocznego zawartości, kontroli odstępów, kerningu, dołączenia znaku, aktywnych selektorów warstw/głównych oraz narzędzi wyszukiwania/flagowania.

## Odkrywanie funkcji: szybka pomoc i obszary robocze

FontLab 7 zawiera wbudowany system **Szybkiej Pomocy**. Najechanie kursorem na dowolną kontrolkę interfejsu użytkownika i przytrzymanie `++F1++` (lub `++Fn+F1++`) powoduje wyświetlenie kompaktowego dymku z objaśnieniami. Dotknięcie `++F1++` włącza ten tryb na stałe. Aby uzyskać bardziej szczegółowy kontekst, `++Shift+F1++` otwiera dedykowany **Panel pomocy**.

Aby zoptymalizować środowisko, skonfiguruj układ i wybierz **Okno > Obszary robocze > Zapisz obszar roboczy**. Możesz zapisać niestandardowe konfiguracje dla określonych przepływów pracy:- **Przestrzeń robocza rysunku:** nadaje priorytet panelom Płótno, Warstwy i Elementy.
- **Przestrzeń robocza metryk:** podkreśla elementy sterujące odstępami i panel Podgląd.
- **Przestrzeń robocza kodowania funkcji:** skupia się na panelach Funkcje i Wyszukiwania.

> [!TIP] Przywróć te obszary robocze za pomocą **Okno > Obszary robocze** lub użyj skrótów klawiaturowych od `++Opt+Cmd+1++` do `++Opt+Cmd+6++` (macOS), aby natychmiast przełączać układy.

---

# Rozdział 3: Pliki czcionek i formaty

## Natywne formaty robocze

FontLab 7 wykorzystuje do programowania dwa natywne formaty plików: **VFC (FontLab Compact)** i **VFJ (FontLab JSON)**. Te formaty działają jak główne dokumenty produkcyjne (analogicznie do pliku PSD w programie Adobe Photoshop), zachowując wszystkie zastrzeżone elementy projektu — w tym notatki glifów, pinezki, odniesienia do elementów, inteligentne narożniki i aranżacje przestrzeni roboczej — które są odrzucane w skompilowanych formatach.- **VFC (.vfc):** Zastrzeżony, wieloplatformowy format binarny zoptymalizowany pod kątem maksymalnej szybkości, szybkiego odczytu i przechowywania na dysku kompaktowym. Jest to zalecany format do codziennej pracy projektowej.
- **VFJ (.vfj):** Tekstowa reprezentacja formatu natywnego przy użyciu struktur JSON. Choć są większe niż pliki VFC, pliki VFJ są czytelne dla człowieka, co czyni je doskonałymi do analizy opartej na skryptach, zautomatyzowanych przepływów pracy i kontroli wersji.

> [!TIP] W obszarze `Preferencje > Zapisz czcionki` wyłącz pole wyboru **Sesja** podczas zapisywania plików VFJ. Spowoduje to usunięcie przejściowych znaczników czasu ostatniej modyfikacji z pliku, co skutkuje czystymi różnicami podczas śledzenia plików źródłowych za pomocą git lub innych systemów kontroli wersji. Włącz **Prettify VFJ**, aby wydrukować sformatowane wcięcia w sposób czytelny dla człowieka.

## Otwieranie, zapisywanie i eksportowanie

FontLab rozróżnia środowisko pracy od ostatecznej dostawy.- **Otwieranie:** Użyj `Plik > Otwórz czcionki...`, aby załadować pliki. Otwarcie plików nienatywnych (takich jak skompilowane pliki OTF/TTF) uruchamia wewnętrzny proces konwersji. Możesz skonfigurować preferencje konwersji w obszarze `Preferencje > Otwarte czcionki`, aby kontrolować sposób obsługi mapowań CID, zaokrąglania konturów, stref wyrównania i funkcji układu OpenType.
- **Zapisywanie:** Polecenia takie jak `Plik > Zapisz czcionkę` (`Cmd+S`) zapisują wyłącznie w formatach VFC lub VFJ, zachowując historię edycji i ustawienia obszaru roboczego.
- **Eksportowanie:** Aby wygenerować użyteczne czcionki, użyj `Plik > Eksportuj czcionki...`. Kompiluje to źródło do formatów gotowych do dystrybucji, przekształcając wyspecjalizowane konstrukcje (takie jak Smart Corners) w standardowe krzywe Beziera.

## Kopie zapasowe i automatyczne zapisywanie konfiguracji

Aby zapobiec utracie danych, FontLab 7 oferuje solidne, wielopoziomowe mechanizmy tworzenia kopii zapasowych i automatycznego zapisywania, konfigurowane poprzez `Preferencje > Zapisz czcionki`.

Zapisując na istniejącym pliku, możesz wybrać sposób, w jaki aplikacja będzie obsługiwać poprzednią wersję:

1. **Zastąp:** Bezpośrednio zastępuje istniejący plik.
2. **Przenieś do kosza:** Wysyła starszą wersję do kosza systemowego.
3. **Zmień nazwę:** Dołącza znacznik czasu (datę i godzinę) do poprzedniego pliku.Włączenie opcji **Zapisz pliki kopii zapasowej w podfolderze** powoduje automatyczne zapisanie kopii zapasowych o zmienionych nazwach w katalogu `.backup` sąsiadującym z plikiem głównym. Dodatkowo włączenie **Autozapisu** powoduje zachowanie repliki aktywnego obszaru roboczego w tle. W przypadku awarii FontLab po ponownym uruchomieniu poprosi o przywrócenie automatycznie zapisanych projektów; są one bezpiecznie odrzucane po czystym, ręcznym zapisaniu i wyjściu.

## Interoperacyjność i formaty dystrybucji

FontLab 7 zapewnia interoperacyjność o wysokiej jakości w całej branży czcionek:

- **Formaty pulpitu:** Eksportuje standardowe formaty **OTF** (PostScript/CFF) i **TTF** (TrueType).
- **Czcionki internetowe:** Eksportuje **WOFF** i **WOFF2**, przy czym WOFF2 wykorzystuje kompresję Brotli firmy Google, aby uzyskać redukcję rozmiaru pliku o ponad 30%.
- **Source Interchange:** Bezproblemowo wymienia pliki z innymi redaktorami za pośrednictwem opartego na XML **UFO** (Unified Font Object) lub natywnego formatu **.glyphs** (obsługującego potoki Glyphs 2 i 3).
- **Color OpenType:** obsługuje wszystkie główne formaty kolorów, w tym **OpenType SVG** (gradienty wektorowe/bitmapowe), **COLR** firmy Microsoft (warstwowe kolory wektorowe) oraz **sbix** firmy Apple lub **CBDT** firmy Google (kolorowe czcionki oparte na bitmapach).

---# Rozdział 4: Panel okna czcionek

Okno czcionek to centralne centrum dowodzenia służące do zarządzania, organizowania i kontrolowania plików czcionek. Kiedy tworzysz nową czcionkę lub otwierasz istniejący plik, FontLab wyświetla glify w interfejsie o uporządkowanej siatce komórek, prezentując kompleksowy przegląd przestrzeni projektowej.

## Interfejs siatki komórkowej

Główny obszar okna czcionek składa się z wykresu glifów, w którym każda komórka reprezentuje pojedynczy glif. Istniejące glify pokazują swoje odpowiednie kontury na białym tle, podczas gdy puste miejsca na glify są pokazane na szarym tle zawierającym jasnoszary szablon zastępczy. Szablony te służą jako wizualne wskazówki dotyczące oczekiwanej postaci, ale nie zawierają rzeczywistych danych zarysu.

Aby dostosować siatkę do różnych procesów projektowania, możesz dostosować wymiary komórek w stopce za pomocą przycisków szerokości komórki — od wąskiej do bardzo szerokiej (stosunek 16:9), co idealnie sprawdza się w przypadku ligatur i pism kaligraficznych. Dodatkowo menu Kolumny (Kolumny) udostępnia wstępnie ustawione rozmiary komórek (8, 16, 24, 32 lub 64 kolumny w wierszu) lub tryb „Flex” umożliwiający dowolną zmianę rozmiaru za pomocą skrótów klawiaturowych powiększania (`Cmd+=` i `Cmd+-`).> [!WSKAZÓWKA] Pasek boczny listy (◨) stanowi alternatywę dla siatki przypominającą arkusz kalkulacyjny i wyświetla konfigurowalne kolumny dla łożysk bocznych (LSB/RSB), szerokości postępu i innych metadanych komórek. Dwukrotne kliknięcie dowolnej wartości w widoku listy umożliwia natychmiastową edycję bezpośrednio w tekście.

## Nawigacja, metadane i flagowanie

Poruszanie się po siatce okna czcionek jest intuicyjne: kliknij, aby wybrać glif, przeciągnij, aby zaznaczyć sąsiadujące zakresy, lub przytrzymaj „Cmd” (macOS) / „Ctrl” (Windows), aby zaznaczyć nieprzylegające komórki. Jedna komórka pozostaje aktywna jako „bieżący” glif, podświetlona na kolor ciemnoniebieski. Dwukrotne kliknięcie otwiera glif w oknie glifów w celu rysowania.

Każda komórka wyświetla w podpisie kluczowe metadane, które mogą zawierać nazwę glifu, punkt kodowy Unicode, indeks glifu lub inne dane kodowania. Jeśli nazwa glifu nie pasuje do przypisanego punktu kodowego Unicode, FontLab wyświetla żółty wskaźnik jako ostrzeżenie.Aby zarządzać złożonymi projektami, możesz przypisać kolorowe flagi (wcześniej zwane „Znakami”) za pośrednictwem paska właściwości, menu kontekstowego lub paska bocznego. Flagi te oznaczają kolorem tło komórki lub podpis. W sekcji Flaga na pasku bocznym możesz zobaczyć wszystkie unikalne flagi kolorów pogrupowane według ich numerycznej wartości odcienia, wraz z liczbą glifów przypisanych do każdej flagi.

> [!UWAGA] Naciśnięcie klawisza spacji na dowolnej komórce glifu otwiera tymczasowe wyskakujące okienko z informacjami o glifie, pokazujące szczegółowe dane, właściwości Unicode i znaczniki.

## Filtrowanie i przeszukiwanie siatki

FontLab oferuje niezawodne metody filtrowania przy użyciu paska właściwości i paska bocznego w celu wyizolowania określonych zestawów glifów:

- **Kodowanie**: Filtruj według standardowych i niestandardowych plików kodowania (`.enc`), wyświetlając miejsca w kolejności kodowania.
- **Bloki Unicode**: Filtruj według standardowych bloków Unicode (zakresów), aby systematycznie dodawać znaki.
- **Kategorie**: Filtruj według grup typograficznych, takich jak wielkie litery (`_uc_`), małe litery (`_lc_`), znaki interpunkcyjne lub cyfry (`_fig_`).
- **Strony kodowe**: Filtruj według platform docelowych lub starszego kodowania (np. Win-1252, MacOS Roman).
- **Indeks**: Sortuj i filtruj glify według ich wartości indeksu glifów (GID). Gdy jest aktywne, sortowanie ręczne jest wyłączone.Pasek szybkiego wyszukiwania w prawym górnym rogu działa jak filtr ad hoc. Można wyszukiwać według nazwy glifu, nazwy znaku Unicode, zakresu lub skryptu. Obsługuje zapytania składające się z wielu podciągów (np. wpisanie `la ca` spowoduje wyświetlenie „Symboli waluty łacińskiej”, a `cu sy` wyszukanie „Symboli walut”). Wyniki wyszukiwania możesz zapisać jako filtry, przeciągając je do zakładek na pasku bocznym lub klikając przycisk „+” w sekcji Historia wyszukiwania.

---

# Rozdział 5: Nawigacja w oknie glifów

Okno glifów (GW) to główna przestrzeń robocza w FontLab 7, w której rysujesz, edytujesz, odstępujesz, kernujesz i podpowiadasz poszczególne glify lub ciągi składające się z wielu glifów. Dwukrotne kliknięcie dowolnej komórki glifu w oknie czcionek otwiera okno glifów, umieszczając wybrany glif na środku obszaru edycji.

## Płótno edycji i kontrola widoku

Kanwa edycji wyświetla kształty glifów wraz z metrykami, wytycznymi i strukturami konturów. Zarządzanie widokiem jest niezbędne do szczegółowego projektowania wektorów:- **Powiększanie:** Użyj `Cmd + Plus` i `Cmd + Minus` (macOS) lub `Ctrl + Plus` i `Ctrl + Minus` (Windows), aby powiększać i pomniejszać. Naciśnij `Cmd+1`, aby wyświetlić w skali 100%, `Cmd+2`, aby powiększyć zaznaczenie i `Cmd+0`, aby dopasować aktywny glif lub ciąg tekstowy do okna. Możesz także przytrzymać „Cmd+Spacja” i przeciągnąć, aby dynamicznie powiększyć.
- **Preferencje:** W _Preferencje > Okno glifów_ możesz dostosować domyślny współczynnik powiększenia, wielkość kroku powiększenia, prędkość przewijania i to, czy powiększanie jest wyśrodkowane na wskaźniku myszy.

## Linijki, prowadnice i współrzędne

Aby zachować spójność typograficzną, okno glifów zapewnia precyzyjne pomoce wizualne i wskaźniki linijki:- **Linijki:** Przełączaj linijki za pomocą `Cmd+R` (`Widok > Linijki`. Pokazują współrzędne płótna względem linii bazowej, wysokości x i namiarów bocznych (definiując lewą podporę i granicę szerokości wyprzedzenia).
- **Prowadnice:** Przeciągnij z poziomych lub pionowych linijek, aby utworzyć linie pomocnicze. Lokalne wytyczne należą do aktywnego glifu, natomiast wytyczne globalne dotyczą całej czcionki. Kliknij dwukrotnie prowadnicę, aby edytować jej nazwę, dokładne położenie, kolor lub wyrażenia matematyczne we właściwościach prowadnicy.
- **Współrzędne:** FontLab 7 obsługuje zarówno zaokrąglanie współrzędnych w postaci liczb całkowitych, jak i współrzędne ułamkowe (zmiennoprzecinkowe podwójnej precyzji). Wybierz współrzędne ułamkowe, aby zachować gładkość krzywej Beziera i ciągłość węzła G2 w różnych odmianach wzorca, a następnie zaokrąglij je za pomocą opcji „Kontur > Współrzędne okrągłe” w celu ostatecznego eksportu czcionek.

## Paski kontrolne i pasek właściwości

Interfejs wokół płótna dostosowuje się do Twojego przepływu pracy:- **Pasek właściwości:** Umieszczony w górnej części okna, wyświetla kontekstowe elementy sterujące aktywnego narzędzia (np. współrzędne węzła, kąty uchwytów lub opcje wyrównania).
- **Pasek boczny treści:** Zawiera listę główną, aktywne warstwy tekstowe i szybki dostęp do edycji metryk.

## Zakres edycji: kontrola wyłączna a kontrola współdzielona

Domyślnie operacje edycyjne dotyczą wyłącznie aktywnego elementu na bieżącej warstwie głównej. Aby edytować jednocześnie inne obszary, możesz dostosować zakres edycji:

- **Edycja między elementami:** Po włączeniu („Edycja > Edytuj między elementami”) możesz wybierać i edytować węzły należące do różnych elementów wektorowych w tym samym glifie.
- **Edycja między glifami:** Przełącz tę opcję (`Alt+Cmd+E`), aby edytować kontury dowolnego glifu widocznego w ciągu tekstowym, a nie tylko aktywnego.
- **Edycja między warstwami:** Jeśli opcja ta jest aktywna, zmiany można zastosować jednocześnie w wielu warstwach głównych lub w warstwie Maska.

> [!WSKAZÓWKA] Użyj `Shift+Alt+Spacja`, aby przełączyć _Szczegóły między glifami_. Po wyłączeniu nieaktywne glify renderują się jako czyste, wypełnione sylwetki, ukrywając rozpraszające struktury węzłów.

## Tryb tekstowyPrzejdź do narzędzia Tekst („T”), aby przejść do trybu tekstowego. Spowoduje to przekształcenie obszaru rysunku w interaktywny edytor tekstu:

- **Wprowadzanie bezpośrednie:** Wpisz znaki Unicode bezpośrednio na płótnie, aby zobaczyć, jak są one rozmieszczone i kernowane.
- **Notacja glifów:** Wprowadź glify według nazwy, używając składni `/name` (np. `/A/B/C/d.sc`) lub punktów kodowych szesnastkowych (`\u0041`).
- **Wyjście:** Naciśnij „Esc”, aby powrócić do poprzedniego narzędzia do rysowania lub edycji.

---

# Rozdział 6: Podstawowe narzędzia do rysowania wektorowego

FontLab 7 zapewnia potężny zestaw narzędzi do rysowania wektorowego zaprojektowanych specjalnie do projektowania czcionek i inżynierii czcionek. Rysowanie konturów glifów wymaga precyzyjnej kontroli nad krzywymi Béziera, ciągłością węzłów i geometrią kształtu. W tym rozdziale opisano podstawowe narzędzia do tworzenia i edytowania konturów: narzędzia Ołówek, Pióro i Szybkie, a także prymitywy geometryczne i techniki wstawiania węzłów.

## Narzędzie Ołówek (N)

Narzędzie **Ołówek** jest zoptymalizowane pod kątem odręcznego szkicowania i szybkiego prototypowania. Umożliwia projektantom naturalne rysowanie ścieżek bez ręcznego umieszczania poszczególnych punktów kontrolnych Béziera. FontLab automatycznie konwertuje pociągnięcia odręczne na gładkie krzywe Béziera i segmenty linii prostych.- **Rysowanie odręczne:** Przeciągnij, aby naszkicować krzywe. Przytrzymaj klawisz „Alt”, aby narysować linie proste, lub klawisze „Alt+Shift”, aby ograniczyć ścieżkę w poziomie lub w pionie.
- **Zamykanie ścieżek:** Przesuń kursor z powrotem do węzła początkowego; niebieskie kółko wskazuje, że zwolnienie myszy spowoduje zamknięcie konturu.
- **Edycja istniejących konturów:** Dzięki narzędziom _Pióro i ołówek mogą kontynuować pracę na konturze_ włączonym w Preferencjach, rysowanie istniejącego konturu od węzła do węzła płynnie zastąpi lub rozszerzy tę sekcję.

> [!WSKAZÓWKA] Użyj narzędzia Ołówek na tablecie graficznym, aby szybko prześledzić zaimportowane skany tła lub szkice analogowe przed ręcznym dopracowaniem węzłów.

## Narzędzie Pióro (P)

Tradycyjne narzędzie Béziera **Pen** zapewnia całkowitą ręczną kontrolę nad rozmieszczeniem węzłów i kierunkiem uchwytu wektorowego, co ma kluczowe znaczenie dla uzyskania czystych konturów i doskonałej ciągłości węzłów (takiej jak gładkość G1 i G2).- **Tworzenie węzłów:** Kliknij, aby umieścić węzeł narożny. Kliknij i przeciągnij, aby utworzyć gładki węzeł z symetrycznymi punktami kontrolnymi Béziera.
- **Dostosowywanie uchwytów:** Przytrzymaj klawisz Alt podczas przeciągania, aby przerwać wyrównanie uchwytów i utworzyć punkt narożny z asymetrycznymi uchwytami. Przytrzymaj „Shift”, aby ograniczyć kąty uchwytu do przyrostów 45 stopni.
- **Zamykanie i kończenie:** Kliknij węzeł początkowy, aby zamknąć pętlę, lub naciśnij „Esc”, aby pozostawić kontur otwarty.

## Szybkie narzędzie (5)

Narzędzie **Rapid** to inteligentne narzędzie do rysowania typu „kliknięcie po kliknięciu”, które automatycznie określa rozmieszczenie węzłów i uchwyty na podstawie miejsca kliknięcia. Rysuje kwadratowe krzywe Béziera za pomocą specjalnego interfejsu, który automatycznie konwertuje na sześcienne krzywe Béziera podczas przełączania narzędzi.- **Umieszczenie węzła:** Kliknij, aby dodać węzeł prosty; kliknij dwukrotnie (lub `Ctrl+kliknięcie`), aby umieścić gładki węzeł. `Cmd+Alt+Kliknięcie` umieszcza węzeł styczny.
- **Kontrola naprężenia:** Segmenty zakrzywione są tworzone przy użyciu domyślnego naprężenia zdefiniowanego w Informacje o czcionce. Wyższe wartości naprężenia tworzą krzywe supereliptyczne.
- ** Interaktywne korekty:** Przeciągnij dowolny węzeł lub punkt kontrolny podczas rysowania, aby natychmiast zmodyfikować ścieżkę. Kliknij dwukrotnie dowolny węzeł, aby przełączać pomiędzy typami połączeń gładkich i narożnych.

> [!WAŻNE] Włączenie _Narzędzie Rapid zapamiętuje ostatni stan_ w Preferencjach pozwala na ciągłe umieszczanie węzłów tego samego typu bez konieczności podwójnego klikania każdej krzywej.

## Kształty pierwotne (I i O)

Do geometrycznej konstrukcji glifów FontLab zawiera narzędzia **Prostokąt** (`I`) i **Elipsa** (`O`).- **Gesty rysunkowe:** Przeciągnij, aby zdefiniować granice kształtu. Przytrzymaj „Shift”, aby ograniczyć się do kwadratu lub okręgu, i przytrzymaj „Alt”, aby rysować od środka.
- **Wprowadzanie numeryczne:** Kliknij raz na obszarze roboczym, aby otworzyć okno dialogowe Dodaj prostokąt lub Dodaj owal i wprowadź dokładne wymiary.
- **Geometryczne a zakrzywione:** Na pasku właściwości możesz przełączać pomiędzy tradycyjnymi elipsami geometrycznymi a elipsami zakrzywionymi, które uwzględniają parametr Naprężenie czcionki.

## Wstawianie węzłów na ścieżkach

Dodawanie węzłów do istniejących ścieżek ma kluczowe znaczenie dla udoskonalenia ścieżki i dodania szczegółów:

- **Za pomocą Pióra/Rapid Tools:** Najedź kursorem na aktywny segment i kliknij, aby wstawić węzeł narożny (lub kliknij dwukrotnie narzędziem Rapid, aby uzyskać gładki węzeł).
- **Za pomocą narzędzia Kontur (`A`):** Kliknij dwukrotnie dowolny segment, aby wstawić nowy węzeł bez modyfikowania istniejącej geometrii krzywej.

---

# Rozdział 7: Zaawansowana edycja punktów i węzłów

## Typy węzłów: narożnikowe lub gładkie

W FontLab 7 kontury są definiowane przez krzywe Béziera i dwa główne typy węzłów, które określają sposób łączenia segmentów ścieżki.- **Węzły narożne**: Oznaczone czerwonymi, kwadratowymi symbolami, węzły narożne (lub ostre) tworzą ostry kąt pomiędzy dowolnymi dwoma segmentami (prostymi lub zakrzywionymi).
- **Węzły gładkie**: Węzły gładkie, oznaczone zielonymi, okrągłymi symbolami, zapewniają ciągłość styczną. Pomiędzy dwiema krzywymi są to _węzły krzywej_, wyrównujące uchwyty współliniowo. Pomiędzy krzywą a linią prostą stanowią one _węzły styczne_, zmuszające uchwyt do wyrównania z segmentem prostym.

Dwukrotne kliknięcie węzła przełącza go pomiędzy narożnikiem a gładkim.

> [!UWAGA] Nie ma typu gładkiego węzła do łączenia dwóch prostych segmentów. Jeśli są współliniowe, węzeł należy usunąć, aby utworzyć pojedynczy segment.

## Inteligentne węzły: sługa i geniusz

Inteligentne węzły to specjalne właściwości przypisane do węzłów w celu automatyzacji rysowania i śledzenia krzywych.

### Węzły usługowe

Węzeł podrzędny ma swoje współrzędne X, Y lub obie współrzędne powiązane z sąsiednimi węzłami niesłużebnymi. Kiedy przesuwasz sąsiedni węzeł, pozycja węzła podrzędnego jest interpolowana, a jego uchwyty skalują się proporcjonalnie. Jest to idealne rozwiązanie do zachowania proporcji w zaokrąglonych kształtach. Aby to przypisać, kliknij węzeł prawym przyciskiem myszy i wybierz **X-Servant** lub **Y-Servant** z menu kontekstowego.

### Węzły geniuszuWęzły Genius zawsze zachowują ciągłość krzywizny G2 (ultra gładkość). W przeciwieństwie do ciągłości G1, która wyrównuje uchwyty jedynie współliniowo, ciągłość G2 odpowiada szybkości zmiany krzywizny po obu stronach węzła. Kiedy dopasujesz uchwyty węzła Genius, FontLab automatycznie przesuwa pozycję węzła wzdłuż ścieżki, aby zachować idealną krzywą G2.

> [!TIP] Użyj **Widok > Pokaż > Krzywizna**, aby sprawdzić ciągłość G2. Grzebienie krzywizny będą miały taką samą wysokość po obu stronach węzła Genius.

## Kierunek ścieżki i wypełnienia

Każdy kontur ma wyznaczony **Punkt początkowy** (pierwszy węzeł) i kierunek ścieżki, który może być zgodny lub przeciwny do ruchu wskazówek zegara.

- **Punkt początkowy**: Wskazany przez szarą strzałkę kierunkową, gdy włączona jest opcja **Widok > Pokaż > Kierunek konturu**.
- **Zasady nawijania**: Kontury PostScript (typ 1) wymagają wypełnienia ścieżek w kierunku przeciwnym do ruchu wskazówek zegara (czarny) i niewypełnienia ścieżek zgodnych z ruchem wskazówek zegara (wycięcia/dziury). W konturach TrueType obowiązuje odwrotna zasada.

Podczas gdy FontLab 7 automatycznie koryguje kierunki ścieżek i rozwiązuje nakładanie się podczas eksportu, możesz ręcznie odwrócić kierunki konturów lub zmienić punkt początkowy, klikając prawym przyciskiem myszy węzeł i wybierając **Utwórz punkt początkowy**.## Mechanika selekcji

Precyzyjna edycja węzłów jest niezbędna, ponieważ przesuwanie konturów bezpośrednio zmienia szerokość glifu i jego położenie boczne. Wymaga to zrozumienia, w jaki sposób FontLab rozróżnia węzły i uchwyty podczas zaznaczania.

- **Wybór indywidualny**: Kliknij bezpośrednio węzeł lub uchwyt. Kliknij z wciśniętym klawiszem Shift, aby dodać lub usunąć punkty z zaznaczenia.
- **Zaznaczenie zaznaczenia**: Przeciągnij prostokąt nad obszarem roboczym. Jego zachowaniem reguluje opcja `Preferencje > Edycja > Wybór markizy ignoruje uchwyty podczas wybierania węzłów. Jeśli ta opcja jest włączona, przeciąganie po obu węzłach i uchwytach powoduje zaznaczenie tylko węzłów. Jeśli markiza zawiera tylko uchwyty, zostaną one zaznaczone.
- **Zaznaczanie lasso**: Przytrzymaj **Alt** podczas przeciągania, aby narysować dowolne lasso, zaznaczając wszystkie zawarte węzły i uchwyty.

> [!WAŻNE] Gdy opcja `Wybór markizy ignoruje uchwyty` jest aktywna, użycie **Markiza z klawiszem Shift** w celu odznaczenia zawsze spowoduje odznaczenie wszystkich przechwyconych elementów, niezależnie od tego, czy są to węzły, czy uchwyty.

---

# Rozdział 8: Manipulacja segmentami i linie TunniModyfikowanie konturów w FontLab 7 wymaga zrozumienia geometrii ścieżki, ciągłości węzłów i zachowań uchwytów. Ścieżki wektorowe składają się z węzłów i krzywych Beziera. Regulacja długości i kątów uchwytów określa napięcie i krzywiznę krzywizny, wpływając na płynność przejść pomiędzy segmentami.

## Edycja symetryczna za pomocą linii Tunni

Podczas edytowania krzywych zdefiniowanych za pomocą dwóch uchwytów sterujących utrzymanie zrównoważonego napięcia jest wyzwaniem. FontLab 7 rozwiązuje ten problem za pomocą **linii Tunni** — wyimaginowanych niebieskich linii kropkowanych łączących pasujące uchwyty Beziera segmentu krzywej. Umożliwiają jednoczesną regulację napięcia i proporcji uchwytów.

Aby przełączyć linie Tunni, dotknij „L” lub wybierz **Widok > Linie Tunni**. Najechanie kursorem pomiędzy uchwytami wyświetla linię Tunni i jej centralny punkt kontrolny (duża niebieska kropka).- **Edycja symetryczna:** Przeciągnij linię Tunni lub przytrzymaj „Shift” i przeciągnij punkt kontrolny, aby zsynchronizować oba uchwyty.
- **Edycja asymetryczna:** Przeciągnij punkt kontrolny bez „Shift”, aby dostosować tylko jeden uchwyt.
- **Dostosowanie klawiatury:** Wybierz linię Tunni i naciśnij „Alt” ze strzałkami:
  - `Alt + Lewo/Prawo` przesuwa punkt Tunni równolegle, wydłużając jeden uchwyt i skracając drugi.
  - `Alt + Góra/Dół` przesuwa go prostopadle, zwiększając lub zmniejszając napięcie krzywej.
- **Edycja wsadowa:** **Kontur > Edytuj linie Tunni** (`Cmd + Alt + L`) aktywuje linie Tunni dla wybranych segmentów; naciśnij „Esc”, aby dezaktywować.

> [!UWAGA] Regulacja napięcia za pomocą linek Tunni pomaga zachować ciągłość krzywizny G2, niezbędną do płynnego przejścia krzywizn.

## Modele usuwania węzłów i segmentów

FontLab 7 oferuje dwa różne modele usuwania węzłów i segmentów: zachowanie krzywej i oderwanie ścieżki.- **Usunięcie z zachowaniem krzywej (Backspace):** Usuwa wybrany węzeł lub uchwyt, pozostawiając kontur zamknięty. FontLab ponownie oblicza pozostałe uchwyty, aby przybliżyć oryginalny kształt ścieżki.
- **Awulsja ścieżki (Usuń):** Usuwa węzeł i przerywa kontur, pozostawiając otwarte punkty końcowe.
- **Usunięcie segmentu:** Naciśnięcie „Backspace” usuwa segment i jego węzły, ale pozostawia kontur zamknięty. Naciśnięcie „Usuń” powoduje usunięcie tylko segmentu, pozostawiając węzły końcowe nienaruszone, ale przerywając kontur.

## Narzędzie Nożyczki i zapętlone rogi

**Narzędzie Nożyczki** („Q”) rozłącza węzły, dzieli ścieżki i zarządza nakładaniem się.

- **Odłączanie:** Kliknięcie węzła powoduje przecięcie konturu i wydłużenie sąsiednich segmentów.
- **Zalewki atramentowe:** Kliknięcie węzła z wciśniętym klawiszem Shift powoduje jego zduplikowanie i rozdzielenie według odległości w **Informacje o czcionce > Wymiary czcionki > Szerokość zalewki atramentowej**.
- **Zapętlone narożniki:** Kliknięcie ostrego węzła z wciśniętym klawiszem Alt tworzy zamknięty, samoprzecinający się „zapętlony narożnik”. Pętle rozciągające się do wypełnionych obszarów to _wewnętrzne zapętlone rogi_; te rozciągające się na puste obszary to _zewnętrzne zapętlone rogi_. Pętle te utrzymują dopasowującą liczbę węzłów dla czcionek zmiennych.

## Filtry upraszczające konturyDo automatycznej optymalizacji FontLab udostępnia dwa filtry:

- **Uprość** (`Alt + Cmd + B`): Usprawnia kontury, usuwa zbędne węzły i dodaje węzły ekstremalne. Konwertuje krzywe TrueType na PostScript i może zmieniać kształt.
- **Oczyszczanie:** Usuwa niepotrzebne węzły bez dodawania nowych, utrzymując kształt konturu bliżej oryginału.

> [!WSKAZÓWKA] Użyj **narzędzia Gumka** (`2`), aby uzyskać zlokalizowane uproszczenie poprzez kliknięcie węzła z wciśniętym klawiszem Ctrl, a następnie kliknięcie innego węzła na tym samym konturze.

---

# Rozdział 9: Odniesienia do elementów i komponowanie

FontLab 7 wykorzystuje elastyczne, obiektowe podejście do konstruowania glifów poprzez **Elementy**. Zamiast polegać na prostych, płaskich konturach, FontLab umożliwia tworzenie złożonych glifów przy użyciu indywidualnych elementów projektu, które można ponownie wykorzystać. W tym rozdziale wyjaśniono mechanikę komponowania, koncepcję odniesień do elementów oraz sposób zarządzania nimi w projekcie czcionki.

## Projektowanie i elementy oparte na komponentachW profesjonalnym projektowaniu czcionek glify często składają się z odrębnych części, takich jak łodygi, szeryfy lub znaki diakrytyczne. W FontLab 7 każdy rysunek wektorowy, obraz lub pole tekstowe jest traktowane jako **Element**. Warstwa glifów może zawierać jeden element lub złożenie wielu elementów.

W przeciwieństwie do warstw standardowych, które oddzielają całe projekty główne (takie jak Regularne i Pogrubione) lub przestrzenie współrzędnych, elementy są blokami konstrukcyjnymi w ramach jednej warstwy. Komponowanie polega na łączeniu tych bloków w kompletne glify, na przykład łącząc elementy „e” i „ostre” w celu utworzenia „eacute”.

## Odniesienia do elementów a komponenty

Podczas gdy inne edytory czcionek używają „komponentów” do łączenia konturów jednego glifu z innym, FontLab 7 wykorzystuje **Odniesienia do elementów**. Odniesienie do elementu to łącze do elementu źródłowego. Kluczową różnicą jest to, że elementy nie muszą istnieć w czcionce jako samodzielne glify; mogą znajdować się wyłącznie w **Galerii** czcionki lub jako elementy niezamapowane.

Kiedy kopiujesz element i wklejasz go jako odniesienie (używając opcji „Edycja > Wklej specjalnie > Linki” lub „Element > Odniesienie”), tworzysz aktywny klon.- **Łączenie na żywo:** Edycja krzywych Beziera, ciągłości węzłów (status G1 lub G2) lub współrzędnych jednego odniesienia do elementu natychmiast aktualizuje wszystkie pozostałe wystąpienia w całej czcionce.
- **Nieniszczące transformacje:** każde wystąpienie odniesienia można w unikalny sposób skalować, obracać, odbijać lustrzanie lub przesuwać bez przerywania połączenia z konturami źródłowymi.
- **Niezależne metryki:** Szerokość postępu i łożyska boczne złożonego glifu pozostają regulowane, podczas gdy wewnętrzne pozycjonowanie odniesienia jest aktualizowane dynamicznie.

> [!WSKAZÓWKA] Użyj odwołań do elementów w przypadku wspólnych cech, takich jak szeryfy, tematy lub akcenty diakrytyczne. Zapewnia to spójność stylistyczną i przyspiesza globalne zmiany projektu.

## Zarządzanie elementami

FontLab 7 udostępnia kilka narzędzi i paneli do porządkowania elementów i manipulowania nimi:

### Panel Elementy i lista warstw

**Panel Elementy** wyświetla hierarchiczną strukturę aktywnej warstwy. Tutaj możesz nazwać elementy, wyświetlić ich odniesienia i zmienić ich kolejność. Zmiana kolejności elementów zmienia ich stos renderowania, co ma kluczowe znaczenie w przypadku kolorowych czcionek lub nakładających się kształtów.

### Panel Galerii**Panel Galeria** pełni funkcję repozytorium wszystkich elementów czcionki. Możesz przeciągnąć elementy z płótna do Galerii, aby zapisać je do wykorzystania w przyszłości, lub przeciągnąć je z Galerii do glifu, aby umieścić odniesienie.

### Rozkładanie odniesień

Jeśli chcesz dokonać unikalnych zmian w instancji elementu bez wpływu na inne glify, musisz go **rozłożyć**.

1. Wybierz odniesienie do elementu w oknie Glif.
2. Wybierz „Element > Rozłóż” (lub kliknij ikonę rozkładania w panelu Elementy).
3. Odniesienie jest konwertowane na niezależne, lokalne kontury Beziera.

> [!WAŻNE] Rozkładanie jest destrukcyjne i nie można go cofnąć po zapisaniu pliku. Połączenie z elementem nadrzędnym zostaje trwale zerwane.

---

# Rozdział 10: Praca z kolorami i próbkami

FontLab 7 zapewnia kompleksowy zestaw narzędzi kolorystycznych przeznaczonych do zarządzania przepływem prac projektowych i projektowania wielokolorowych, warstwowych czcionek OpenType. Kolor można zastosować jako metadane do oznaczania komórek glifów w interfejsie lub bezpośrednio do konturów glifów jako właściwości obrysu i wypełnienia wektora.

## Wizualna organizacja kolorówKolor jest niezbędnym narzędziem organizującym w projektowaniu czcionek. FontLab 7 rozróżnia organizację na poziomie interfejsu użytkownika (taką jak oznaczanie glifów w celu śledzenia postępu projektu) i przypisywanie kolorów na poziomie konspektu (takie jak tworzenie kolorowych czcionek za pomocą tabel SVG lub COLR/CPAL).

## Flagowanie komórek

Flagowanie komórek (w FontLab Studio 5 nazywane „znacznikami glifów”) umożliwia zastosowanie podświetlenia tła i koloru podpisu do komórek glifów w oknie czcionek. Flagowanie to doskonały sposób na wizualne kategoryzowanie glifów według stanu, typu (wielkie i małe litery, cyfry) lub pisma.- **Stosowanie flag:** Zaznacz komórki glifów i wybierz jeden z pięciu predefiniowanych kolorów flag (czerwony, niebieski, zielony, magenta, cyjan) z nagłówka okna czcionek lub z podmenu **Flaga** menu kontekstowego.
- **Flagi niestandardowe:** Wybierz opcję **Niestandardowe...**, aby określić niestandardową wartość odcienia (0–360) za pomocą suwaka lub bezpośredniego wpisu numerycznego.
- **Usuwanie flag:** Wybierz oznaczone glify i kliknij **Brak flag** w nagłówku lub menu kontekstowym.
- **Pasek boczny i filtrowanie:** Na pasku bocznym okna czcionek, sekcja **Flaga** wyświetla wszystkie aktywne flagi wraz z liczbą glifów przypisanych do każdej z nich. Kliknij flagę na pasku bocznym, aby przefiltrować okno czcionek. Włącz opcję **Ukryj niefiltrowane glify**, aby wyświetlić tylko oflagowany podzbiór, lub pozostaw tę opcję wyłączoną, aby zgrupować oflagowane glify na górze.
- **Wybór:** Użyj opcji **Wybierz > Ta sama flaga** z menu kontekstowego, aby wybrać wszystkie glify współdzielące flagę aktywnego glifu.

> [!WSKAZÓWKA] Flagowanie komórek nie wpływa na wizualne kontury eksportowanej czcionki, ale FontLab używa tych metadanych podczas programowania do filtrowania, sortowania i przetwarzania wsadowego.

## Obrysuj kontury i wypełnieniaAby zaprojektować kolorowe czcionki, możesz zastosować kolory obrysu i wypełnienia do konturów glifów. W FontLab 7 kolor jest stosowany do poziomu **Elementu**, a nie do poszczególnych konturów lub węzłów. Kontury należące do tego samego elementu muszą mieć ten sam obrys i wypełnienie, ale oddzielne elementy lub odniesienia do elementów w obrębie jednego glifu można kolorować niezależnie.

**Panel kolorów** (**Okno > Panele > Kolor**) posiada trzy tryby interfejsu: koło, suwaki i pudełko.

- Aby pokolorować kontur konturu, kliknij niewypełnione kółko w lewym górnym rogu panelu, wybierz kolor i kliknij **Zastosuj**.
- Aby pokolorować wypełnienie konturowe, kliknij wypełnione kółko, wybierz kolor i kliknij **Zastosuj**.
- Aby zastosować kolory wsadowo, zaznacz wiele komórek w oknie czcionek. Przytrzymaj klawisz Alt podczas klikania **Zastosuj**, aby przypisać kolor do bieżącej warstwy wszystkich wybranych glifów.

## Panel Próbki

Podczas gdy Panel kolorów pełni funkcję selektora, **Panel próbek** (**Okno > Panele > Próbki**) pełni rolę repozytorium predefiniowanych kolorów, umożliwiając przypisanie spójnych właściwości stylu w całej rodzinie czcionek.- **Tryby wyświetlania:** Przełącz między **Trybem listy** (pokazuje próbki z nazwami) a **Trybem tabeli** (wyświetla zwartą siatkę kolorowych ikon).
- **Tworzenie próbek:** Wymieszaj kolor w panelu kolorów, a następnie kliknij przycisk **Dodaj kolor (+)** na pasku stanu panelu próbek, aby go zapisać.

## Zarządzanie bibliotekami palet

Zarządzaj grupami próbek, klikając ikonę palety na pasku stanu Próbki, aby otworzyć okno dialogowe **Palety**. Tutaj możesz dodawać, powielać, zmieniać nazwy i usuwać palety. Niestandardowe palety można zapisać w postaci plików „.palettes”, co idealnie nadaje się do organizowania kategorii stylów i udostępniania konfiguracji kolorów między różnymi projektami.

> [!WAŻNE] Podczas eksportowania czcionek kolorowych FontLab automatycznie generuje tabele CPAL (paleta kolorów) i COLR lub tabele SVG, w zależności od profilu eksportu.

---

# Rozdział 11: Importowanie grafiki i automatyczne śledzenie

FontLab 7 oferuje solidne narzędzia do konwersji fizycznych szkiców, obrazów rastrowych i zewnętrznych szablonów wektorowych w precyzyjne, gotowe do edycji kontury glifów. Projektanci czcionek mogą bezpośrednio importować grafikę wektorową lub wklejać obrazy bitmapowe, korzystając z zaawansowanych filtrów i parametrów automatycznego śledzenia w celu wygenerowania czystych ścieżek Beziera.## Importowanie grafiki wektorowej i bitmapowej

Obsługa FontLab różni się w zależności od tego, czy pracujesz z grafiką wektorową, czy plikami bitmapowymi:

- **Grafika wektorowa (SVG, EPS, PDF, AI):** Możesz importować pliki wektorowe za pomocą opcji „Plik > Importuj > Grafika” lub kopiując i wklejając bezpośrednio z edytorów wektorów. Podczas wklejania FontLab obsługuje zarówno starsze formaty **AICB** (idealne dla ścieżek monochromatycznych), jak i **PDF** (idealne dla złożonych projektów wielokolorowych, masek przycinających lub grafik z Affinity Designer i Sketch). Okno dialogowe _Wklej lub importuj grafikę_ umożliwia wybór pomiędzy importem **Elementów i kolorów** (zachowuje obrys, wypełnienie i kolor) lub **Tylko kontury** (ignoruje styl i automatycznie zaokrągla współrzędne do jednostek całkowitych).
- **Pliki bitmapowe (PNG, JPG, BMP, TIFF):** Obrazy rastrowe są importowane jako elementy obrazu tła. Domyślnie 1 piksel na obrazie rastrowym odpowiada 1 jednostce czcionki. Aby uzyskać optymalną rozdzielczość, szkice projektowe należy przeskalować w taki sposób, aby kluczowe wymiary (takie jak wysokość zakrętki) odpowiadały docelowemu rozmiarowi modułu UPM (np. rysując wielką literę „H” o wysokości 700 pikseli w przypadku wysokości zagłówka wynoszącej 700 jednostek).> [!WSKAZÓWKA] Jeśli grafika wektorowa ma współrzędne ułamkowe, włącz preferencje zaokrąglania współrzędnych, aby podczas importu automatycznie wyrównywać ścieżki do siatki czcionek.

## Przygotowanie bitmap poprzez panel obrazu

Przed automatycznym śledzeniem oczyść swoje szkice rastrowe za pomocą **Panelu obrazu** („Okno > Panele > Obraz”). Wybierz element obrazu i zastosuj te nieniszczące filtry:

- **Usuń tło:** Izoluje rysunek glifów od tła papierowego.
- **Usuwanie plamek / redukcja szumów:** Usuwa artefakty skanowania, kurz i niepotrzebne piksele.
- **Rozmycie gaussowskie i próg:** Lekkie rozmycie obrazu i zastosowanie progu (w oparciu o jasność, krycie lub kolor) wyostrza ostre krawędzie, zamieniając pikselowane gradienty w czarno-białe kształty o wysokim kontraście.

## Parametry automatycznego śledzenia

Aby przekonwertować przygotowany obraz zaznacz go i wybierz `Element > Obraz > Autotrace...`. Okno dialogowe oferuje podgląd w czasie rzeczywistym i zawiera trzy kluczowe suwaki umożliwiające kontrolę początkowego generowania konturu:1. **Tolerancja śledzenia:** Kontroluje, jak blisko ścieżka podąża za granicami pikseli. Wartość 1 dokładnie podąża za krawędziami, podczas gdy wyższe wartości podążają luźno, dając prostsze segmenty.
2. **Odległość dopasowania krzywej:** Dopuszczalny błąd aproksymacji krzywej. Niższe wartości generują więcej węzłów; wyższe wartości dają mniej węzłów i bardziej płaskie segmenty krzywych.
3. **Kąt prosty:** Określa próg konwersji krzywych na linie proste. Wyższe wartości faworyzują punkty narożne i linie proste.

W obszarze **Wynik śledzenia to** wybierz pomiędzy **Konturami PS** (Bezier sześcienny), **Konturami TT** (Bezier kwadratowy) lub **Tylko linie**.

> [!WAŻNE] Przetwórz swój ślad, zaznaczając opcję **Węzły na ekstremach**, aby automatycznie umieszczać węzły na maksimach krzywej poziomej i pionowej, co jest krytyczne dla renderowania i podpowiedzi.

## Śledzenie procesów roboczych i wskazówki dotyczące instrukcji

Po automatycznym śledzeniu wybierz opcję **Zachowaj**, **Usuń** lub **Przenieś do maski** obrazu źródłowego. Przeniesienie obrazu na warstwę Maska ze zmniejszonym przezroczystością (np. 20–30%) pozwala zachować oryginalny szkic jako szablon wizualny do ręcznego rysowania i dokładnego dopasowania konturu.W przypadku arkuszy zawierających całe alfabety umieść zeskanowaną kompozycję na Szkicowniku i wybierz opcję „Element > Obraz > Oddziel i obrysuj”. FontLab podzieli arkusz na poszczególne elementy glifów, korzystając z ustawień separacji optycznej i automatycznie prześledzi je w jednej partii.

---

# Rozdział 12: Zarządzanie warstwami i maskami

## Panel Warstwy i Wzorce

Panel Warstwy i wzorce (**Okno > Panele > Warstwy i wzorce**) to centralne centrum zarządzania wielowarstwowymi konstrukcjami glifów, projektami wzorcowymi i konturami pomocniczymi w FontLab 7. Panel ma uporządkowaną hierarchię: lokalny pasek narzędzi na górze, przewijaną listę warstw pośrodku, zwijaną sekcję właściwości i pasek stanu na dole.

Na liście warstw każdy wpis wyświetla swoją nazwę, podgląd miniatury, liczbę elementów składowych i kolumny stanu dotyczące widoczności, blokowania, atrybutów warstwy usług i wizualizacji szkieletowej. Wizualna informacja zwrotna jest oznaczona kolorami, aby wskazać zgodność interpolacji:- **Pogrubione nazwy:** wskazują główne warstwy czcionek lub glifów, które przyczyniają się do powstania różnic.
- **Bladozielony:** Master jest w pełni kompatybilny z interpolacją.
- **Żółty:** Master jest kompatybilny, ale kolejność konturów lub węzłów jest inna.
- **Bladoczerwony:** Master jest niezgodny, co wskazuje na niedopasowaną liczbę punktów lub konturów.
- **Szara nazwa („#instancja”):** Reprezentuje dynamicznie interpolowaną instancję wirtualną.

## Warstwy główne a warstwy usługowe i pomocnicze

FontLab 7 rozróżnia warstwy narzędziowe, które można eksportować i których nie można eksportować:

- **Warstwy główne:** Definiują granice przestrzeni projektowej dla czcionek zmiennych. Zawierają podstawowe kontury Béziera, kotwice i szerokości zaawansowane, które są eksportowane do formatów ostatecznych.
- **Warstwy usług:** Aktywacja atrybutu usługi („_usługa”) powoduje ukrycie warstwy w oknie czcionek i panelu podglądu. Warstwy usług nie eksportują ani nie uczestniczą w interpolacji.
- **Tło i zablokowane warstwy:** Warstwy można przenieść na tło (na dół stosu) lub zablokować, aby zapobiec przypadkowym edycjom wektorów.
- **Tryb szkieletowy:** Renderuje wypełnione kształty wektorowe jako kontury, przydatne do sprawdzania nakładających się ścieżek.> [!UWAGA] Kliknięcie klawiszem Cmd (`++Cmd++` w systemie macOS lub `++Ctrl++` w systemie Windows) nagłówka kolumny z kolorową kropką automatycznie przypisuje unikalne kolory do wszystkich warstw, z wyjątkiem warstw masek.

## Operacje i właściwości warstw

Na pasku stanu możesz dodawać warstwy (`++Cmd+Shift+N++`), powielać je lub usuwać. Sekcja właściwości, przełączana za pomocą paska narzędzi, udostępnia elementy sterujące przezroczystością (0–100%) i przełącznik Autowarstwy. Aktywacja **Auto Layer** blokuje ręczną edycję, zamiast tego automatycznie generuje kontury glifów przy użyciu predefiniowanych lub niestandardowych receptur glifów FontLab.

> [!WSKAZÓWKA] Użyj przycisku **Scal widoczne warstwy** na pasku stanu, aby połączyć widoczne warstwy niebędące usługami przed spłaszczeniem i eksportowaniem.

## Warstwy maski glifów

Warstwa maski to dedykowana warstwa usług powiązana z nadrzędną warstwą projektową, używana do zachowywania tymczasowych stanów wektorowych.- **Tworzenie maski:** Wybierz kontur i wybierz **Narzędzia > Kopiuj do maski** (`++Cmd+M++`).
- **Edycja maski:** Wybierz **Narzędzia > Edytuj maskę** (`++Ctrl+H++`) lub kliknij dwukrotnie kontury maski. Tło płótna zmienia kolor, wskazując tryb edycji maski.
- **Interakcje:** Przełącz **Widok > Przyciągaj > Maska**, aby przyciągać aktywne węzły konturu bezpośrednio do wektorów maski. Użyj **Narzędzia > Zamień z maską** (`++Ctrl+Alt+M++`), aby zamienić kontury pomiędzy głównym konturem a maską.

## Globalny system masek

W przeciwieństwie do masek lokalnych, **Maska globalna** jest szablonem referencyjnym obejmującym całą czcionkę, który jest wyświetlany we wszystkich glifach i warstwach. Nie pojawia się w panelu Warstwy i wzorce.

- **Tworzenie:** Wybierz kontury w dowolnym glifie i uruchom **Narzędzia > Kopiuj do maski globalnej** (`++Shift+Cmd+M++`).
- **Zastosowanie:** Włącz **Widok > Pokaż > Maska globalna** i **Widok > Przyciąganie > Maska globalna**, aby rzutować szablon i przyciągać do niego kontury w przestrzeni projektowej.
- **Czyszczenie:** Uruchom **Narzędzia > Wyczyść maskę globalną** (`++Shift+Cmd+K++`).

---

# Rozdział 13: Korzystanie ze szkicownikaSketchboard to środowisko otwartego płótna FontLab 7 — nieskończony wirtualny pulpit zaprojektowany z myślą o wspieraniu wczesnych etapów projektowania czcionek. W przeciwieństwie do ustrukturyzowanego okna czcionek lub indywidualnych okien glifów, które wymuszają umieszczenie elementów w sztywnych ramkach metrycznych i ścisłej hierarchii glifów, Szkicownik funkcjonuje jako nieograniczony obszar kreślenia. Umożliwia projektantom szkicowanie, importowanie surowych zasobów, śledzenie zeskanowanych dzieł sztuki i formatowanie próbek próbnych w jednym spójnym obszarze roboczym.

## Rysowanie poza siatką czcionek

Na Sketchboardzie możesz tworzyć geometrię wektorową i manipulować nią bez przypisywania jej do określonego punktu kodowego Unicode lub wiązania standardowymi współrzędnymi czcionki. Ta swoboda jest idealna do eksperymentowania z literami, rysowania logotypów lub odkrywania koncepcji krzywych Beziera przed umieszczeniem ich w formalnym miejscu na glify.Możesz używać pełnego zestawu narzędzi do rysowania FontLab — w tym narzędzi Rapid, Pióro, Ołówek i Pędzel — bezpośrednio na płótnie. Podczas rysowania możesz udoskonalać węzły wektorów, zarządzać uchwytami i wymuszać ciągłość węzłów (taką jak ciągłość krzywizny G1 lub G2), nie martwiąc się o szerokości postępów, nośności boczne lub metryki pionowe. Gdy kształt wektorowy będzie już zadowalający, możesz przekształcić go w element i przeciągnąć bezpośrednio do komórki w panelu Mapa czcionek, natychmiast promując kompozycję do standardowego glifu.

> [!WSKAZÓWKA] Aby szybko zamienić serię odłączonych rysunków na Szkicowniku w glify, zaznacz je narzędziem Element (V) i wybierz **Element > Umieść jako glify > Wybrane elementy**.

## Pola tekstowe i przykładowe ciągi znaków

Sketchboard to także solidne narzędzie do sprawdzania i testowania typografii. Wybierając narzędzie Tekst i klikając w dowolnym miejscu obszaru roboczego, możesz utworzyć pole tekstowe. Te pola tekstowe nie są wyświetlaczami statycznymi; działają jak aktywne, w pełni edytowalne przykładowe ciągi wieloglifowe, korzystając z dowolnej aktywnej czcionki aktualnie otwartej w FontLab.Wszelkie modyfikacje konturów, oznaczeń bocznych lub kerningu w polu tekstowym natychmiastowo aktualizują wszystkie wystąpienia tych elementów glifów na obszarze roboczym i samą otwartą czcionkę. Pola tekstowe obsługują trzy różne tryby zawijania:

1. **Ciągły ciąg**: Utrzymuje przykładowy tekst w jednej linii, co jest idealne do testowania ustawień rytmu wyrazów i nagłówka.
2. **Automatyczne zawijanie bloku**: Zawija tekst wewnątrz prostokątnej ramki o zmiennym rozmiarze, aby przetestować tekstury akapitu.
3. **Widok tabeli**: Umieszcza każdy znak w osobnej komórce, umożliwiając przejrzystą kontrolę metryczną obok siebie.

> [!UWAGA] FontLab automatycznie zapisuje pola tekstowe powiązane z otwartą czcionką w odpowiednim pliku VFC lub VFJ. Jeśli zamkniesz czcionkę, jej pola tekstowe znikną, ale po ponownym otwarciu czcionki pojawią się ponownie w dokładnie tych samych pozycjach.

## Importowanie grafiki i katalogów

Rozpoczynając projekt od rysunków fizycznych, Sketchboard upraszcza przetwarzanie surowej grafiki. Możesz importować duże pliki graficzne lub katalogi zeskanowanych obrazów, korzystając z opcji **Plik > Importuj > Grafika**. FontLab obsługuje formaty wektorowe (EPS, SVG, AI kompatybilne z PDF) i standardowe obrazy bitmapowe.Po zaimportowaniu możesz użyć opcji **Element > Obraz > Oddziel i prześledź**, aby optycznie podzielić zeskanowany arkusz liter na poszczególne komponenty glifów i automatycznie prześledzić je w czyste kontury Beziera.

## Eksportowanie szkicownika

Aby udostępnić próbki lub wyeksportować układy, możesz bezpośrednio wydrukować zawartość Szkicownika za pomocą **Plik > Eksportuj > Zawartość okna**. To polecenie eksportuje płótno do wektorowych formatów PDF lub SVG, zachowując nie tylko kształty konturów i kolorowe mapy bitowe, ale także linie pomocnicze, wskazówki, strefy wyrównania i metryki.

---

# Rozdział 14: Odstępy i łożyska boczne

Aby zaprojektować funkcjonalny krój pisma, odstępy są tak samo ważne jak rysowanie konturów. W FontLab 7 odstępami zarządza się za pomocą poziomych metryk glifów, które określają położenie poszczególnych znaków względem siebie. Kontrolowanie tego rytmu przestrzennego wymaga jasnego zrozumienia wymiarów poziomych, narzędzia Metryki i systemów dynamicznych połączeń.

## Definicje metryk poziomych

Poziome odstępy glifów zależą od czterech podstawowych właściwości przestrzennych:- **Szerokość ramki ograniczającej (BBox):** Fizyczna szerokość konturów glifu, mierzona od skrajnego lewego punktu konturu (lewa krawędź konturu) do skrajnego prawego punktu (prawa krawędź konturu).
- ** Lewe łożysko boczne (LSB):** Odległość pomiędzy początkiem glifu (punkt zerowy na osi poziomej) a skrajną lewą krawędzią obwiedni. Reprezentuje ujemną lub dodatnią białą przestrzeń po lewej stronie glifu.
- **Prawe łożysko boczne (RSB):** Odległość między skrajną prawą krawędzią ramki ograniczającej a granicą szerokości wyprzedzenia.
- **Szerokość zaliczki:** Całkowita przestrzeń pozioma przypisana do glifu. Wartość ta określa odległość poziomą, o jaką przesuwa się kursor tekstowy po wpisaniu znaku. Jest to suma LSB, szerokości BBox i RSB.

> [!UWAGA] Łożyska boczne mogą być dodatnie (dla typowego rozstawu) lub ujemne (kiedy części konturu, takie jak szeryfy litery „T” lub „f”, wychodzą poza granicę szerokości wyprzedzenia).

## Narzędzie Metryki i pasek właściwości

Aby edytować te wartości, aktywuj **narzędzie Metryki**, klikając jego ikonę na pasku narzędzi lub naciskając „M”. Jeśli żadne okno glifów nie jest otwarte, aktywacja narzędzia automatycznie otworzy okno dla wybranego glifu.W trybie metryki aktywny glif jest podświetlany kontrastującymi liniami bocznymi. Jeśli te linie są ukryte, kliknij przycisk **Pokaż elementy sterujące odstępami** na pasku właściwości. Pasek właściwości Metryka wyświetla edytowalne pola dla **L** (LSB), **R** (RSB) i **W** (Szerokość).

Programiści mogą edytować odstępy na trzy sposoby:

1. Przeciągnij linie boczne lub uchwyty trójkątów bezpośrednio do okna Glifów.
2. Klikanie i przeciąganie samego glifu, aby ponownie rozmieścić LSB i RSB bez zmiany całkowitej szerokości przesuwania (lub przeciąganie z wciśniętym klawiszem Alt w celu dostosowania szerokości przesuwania).
3. Wprowadzanie wartości bezpośrednio w polach paska właściwości, Tabeli metryk lub panelu Glif.

> [!WSKAZÓWKA] Naciśnięcie klawisza średnika (`;`) w trybie Metryki uruchamia algorytm automatycznego odstępu FontLab, który natychmiast przypisuje optyczne namiary boczne do bieżącego glifu.

## Wiążące łożyska boczne i pochylona kursywa

FontLab 7 umożliwia projektantom łączenie metryk przy użyciu **wyrażeń połączonych metryk**. Zamiast wprowadzać liczby ręcznie, możesz wprowadzić nazwę glifu (np. „o” lub „H”) w polach LSB, RSB lub Szerokość. FontLab obsługuje podstawowe operacje matematyczne (np. `o * 1.05 + 10`).Aby połączyć metryki pomiędzy różnymi wzorcami, użyj przedrostka dwukropka (np. `:Regular` lub `:Regular * 1.1`). Aby uzyskać automatyczne aktualizacje, włącz **Czcionka > Aktualizacja na żywo > Dane na żywo**.

W przypadku czcionek kursywy, boczne należy mierzyć wzdłuż skosu. Włącz opcję **Widok > Zastosuj kąt pochylenia do metryk** (lub włącz opcję **Preferencje > Siatka > Podążaj za kątem pochylenia czcionki**), aby pochylić siatkę metryk. Dzięki temu współrzędne LSB i RSB są obliczane równolegle do osi kursywy, zachowując spójność wizualną w projektach pochyłych.

---

# Rozdział 15: Klasy kerningu i wyjątki

Kerning dostosowuje odstęp poziomy pomiędzy określonymi parami glifów, aby uzyskać wizualnie spójne odstępy, uzupełniając domyślne oznaczenia boczne. Chociaż kerning płaski (od glifów do glifów) jest prosty, może znacznie rozdęć pliki czcionek. Aby zoptymalizować tabele GPOS, FontLab 7 wykorzystuje kerning oparty na klasach OpenType.

## Klasy kerningu lewego i prawego

Aby efektywnie zarządzać kerningiem, glify o podobnych kształtach optycznych są pogrupowane w klasy kerningu. Ponieważ glif zachowuje się inaczej w zależności od tego, czy pojawia się po lewej czy prawej stronie pary, FontLab 7 rozróżnia:- **1. klasa kerningu (lewa strona):** Stosowana, gdy glif znajduje się po lewej stronie pary. Na przykład glify takie jak „O”, „Q” i „C” mają ten sam wskaźnik klasy dla ich prawego namiaru.
- **Druga klasa kerningu (prawa strona):** Stosowana, gdy glif znajduje się po prawej stronie pary. Na przykład glify takie jak „O”, „U” i „D” mają ten sam wskaźnik klasy dla swoich lewych łożysk bocznych.

Glif może należeć do jednej klasy pierwszej i jednej klasy drugiej. W każdej klasie wyznaczony **kluczowy glif** (lub lider klasy) definiuje relację odstępów dla całej grupy.

> [!WAŻNE] Glif nie może należeć do wielu klas po tej samej stronie. Takie postępowanie powoduje konflikty uniemożliwiające kompilację tabeli GPOS.

## Przebieg pracy i wyjątki związane z kerningiem klas

Aby zbudować proces kerningu klas, projektanci grupują glify w lewą i prawą klasę i definiują kerning dla liderów klas. W przepływie pracy między klasami dostosowanie odstępu między dwoma kluczowymi glifami powoduje automatyczne zastosowanie tego dostosowania do wszystkich kombinacji glifów w tych klasach. To znacznie zmniejsza obciążenie związane z definiowaniem korekt parami dla każdej kombinacji.Jednak niektóre pary wymagają unikalnych odstępów, co odbiega od reguły klasowej. Są one traktowane jako **wyjątki kerningu**:

1. Wybierz parę w oknie glifów z aktywnym narzędziem **Kerning** (`K`).
2. Znajdź **ikony kłódki** na pasku właściwości lub w panelu Kerning obok aktywnych glifów.
3. Kliknij ikonę kłódki, aby ją odblokować, odłączając glif od klasy dla tej pary.
4. Dostosuj wartość kerningu, aby zapisać wyjątek specyficzny dla glifu, zastępując regułę klasy.

> [!TIP] Ogranicz wyjątki do minimum. Nadmierne wyjątki zawyżają rozmiary tabel GPOS i mogą powodować problemy z renderowaniem w starszych środowiskach.

## Panel par i wyrażeń

Systematyczne testowanie ma kluczowe znaczenie dla jakości kerningu. Użyj panelu **Pary i frazy** (`Okno > Panele > Pary i frazy`), aby sprawdzić kombinacje:

- **Wybór listy:** Załaduj predefiniowane listy popularnych par, słów lub niestandardowych tekstów.
- **Filtrowanie:** Filtruj listę, aby wyświetlić tylko aktywne pary, pary klas lub określone postacie.
- **Nawigacja:** Kliknij dwukrotnie dowolną parę w panelu, aby natychmiast wyświetlić ją w oknie glifów w celu szybkiej edycji.

## Szybka kontrola kerningu i edycjaGdy narzędzie Kerning jest aktywne, możesz edytować wartości kerningu wizualnie lub numerycznie:

- **Wizualne przeciąganie:** Przeciągnij aktywny glif lub interaktywny uchwyt kerningu pomiędzy glifami, aby dostosować odstęp.
- **Skróty klawiaturowe:** Naciśnij klawisze strzałek „W lewo”/„Prawo”, aby dokonać regulacji co 1 jednostkę, lub przytrzymaj klawisz „Shift”, aby uzyskać krok co 10 jednostek.
- **Pasek właściwości:** Wprowadź dokładne wartości liczbowe bezpośrednio w polu kerningu w górnej części okna.

---

# Rozdział 16: Funkcje układu OpenType

Funkcje układu OpenType przekształcają statyczne glify w dynamiczne, inteligentne systemy typograficzne. Definiując podstawienia glifów i precyzyjne dopasowanie położenia, projektanci mogą zarządzać złożonymi skryptami, ligaturami, kapitalikami, alternatywami kontekstowymi i załącznikami typu „mark to base”. FontLab 7 zapewnia kompleksowe środowisko do pisania, kompilowania, testowania i zarządzania tym kodem układu przy użyciu standardowej składni pliku Adobe Feature File (FEA).

## Panel funkcji

Centralnym centrum zarządzania kodem funkcji jest **panel Funkcje** (Okno > Panele > Funkcje). Tutaj możesz zdefiniować klasy glifów, bloki przedrostków i określone funkcje OpenType (takie jak `liga`, `smcp` lub `kern`.- **Klasy glifów**: Grupuj glify o wspólnych rolach typograficznych (np. małe litery, kapitaliki lub glify podstawowe) w celu usprawnienia zasad. FontLab obsługuje zarówno klasy nazwane (np. `@lc_vowels`), jak i klasy wbudowane.
- **Prefiks**: Dodaj deklaracje globalne, takie jak instrukcje systemu językowego (np. `languagesystem latn dflt;`), które rejestrują funkcje w systemach operacyjnych, silnikach układu i aplikacjach.
- **Funkcje**: Poszczególne bloki zawierające reguły podstawiania i pozycjonowania pogrupowane według czteroliterowych znaczników OpenType.

> [!WSKAZÓWKA] Możesz automatycznie wygenerować standardowe funkcje, wybierając **Utwórz funkcje z informacji o czcionce** w menu panelu. FontLab analizuje nazwy glifów, aby wygenerować reguły dla ligatur, kapitalików i cyfr.

## Pisanie zasad zastępstw i pozycjonowania

Kod funkcji OpenType dzieli instrukcje na dwie główne kategorie: GSUB (podstawianie glifów) i GPOS (pozycjonowanie glifów).

### Podstawienia glifów (GSUB)

Podstawienia zastępują jeden lub więcej glifów glifami alternatywnymi. Do najpopularniejszych zasad substytucji zalicza się:- **Ligatury (`liga`, `dlig`)**: Wiele glifów wejściowych jest zastępowanych pojedynczym glifem złożonym. `sub f i przez f_i;`
- **Małe wielkie litery (`smcp`, `c2sc`)**: Zastępuje standardowe małe lub wielkie litery ich odmianami. `sub a przez a.sc;`
- **Alternatywy kontekstowe (`calt`)**: Zastępuje glif na podstawie otaczającego go kontekstu glifu. `sub f' [tj. e] przez f.short;`

### Pozycjonowanie glifów (GPOS)

Reguły pozycjonowania dostosowują położenie lub szerokość glifów bez ich zastępowania. Jest to niezbędne w przypadku kerningu i umieszczania znaków diakrytycznych:

- **Dopasowanie par (Kerning)**: Przesuwa odległość pomiędzy określonymi parami glifów. „poz Te -50;”.
- **Dołączenie znaku (`mark`, `mkmk`)**: Zakotwicza znaki diakrytyczne do glifów bazowych za pomocą punktów kontrolnych opartych na współrzędnych. `podstawa poz [a] <kotwica 450 600> znak @TOP_MARKS;`

> [!WAŻNE] Podczas definiowania korekt pozycjonowania FontLab tłumaczy kotwice wizualne (takie jak punkty „górne” i „dolne” zdefiniowane w oknie Glifów) bezpośrednio na kod kotwicy GPOS podczas kompilacji.

## Kompilowanie i testowanie funkcjiAby funkcje OpenType mogły działać, muszą zostać skompilowane w tabele binarne. FontLab 7 wykorzystuje zintegrowaną bibliotekę Adobe AFDKO do kompilowania kodu funkcji w aplikacji.

- Aby skompilować, kliknij przycisk **Kompiluj** (ikona odtwarzania) w panelu Funkcje. Wszelkie błędy składniowe lub ostrzeżenia dotyczące kompilacji zostaną wyświetlone w panelu Wyjście.
- Aby przetestować skompilowane funkcje, otwórz **panel podglądu** (Okno > Panele > Podgląd). Wpisz ciągi testowe i przełącz aktywne funkcje z selektora funkcji w panelu, aby zweryfikować podstawienia i pozycjonowanie w czasie rzeczywistym.

## Zarządzanie zewnętrznymi plikami funkcji

W przypadku złożonych przepływów pracy FontLab umożliwia ładowanie i zapisywanie zewnętrznych plików `.fea`. Za pomocą menu panelu Funkcje możesz zaimportować zewnętrzny kod funkcji w celu nadpisania lub dołączenia do istniejących reguł.

> [!UWAGA] Zewnętrzne importy MES są analizowane i mapowane na istniejące glify. Upewnij się, że wszystkie nazwy glifów, do których odwołują się pliki zewnętrzne, dokładnie odpowiadają nazwom glifów występujących w mapie czcionek FontLab.

---

# Rozdział 17: Informacje o czcionkach i konfiguracja osiPanel **Informacje o czcionce** (Plik > Informacje o czcionce) służy jako scentralizowane repozytorium wszystkich metadanych, atrybutów stylu, wskaźników globalnych i parametrów odmian w projekcie FontLab. Dokładne skonfigurowanie tych ustawień ma kluczowe znaczenie dla wygenerowania w pełni funkcjonalnych czcionek OpenType, TrueType i Variable.

## Struktura metadanych informacji o czcionce

Informacje o czcionkach są zorganizowane w hierarchiczne sekcje. Podstawowe metadane obejmują:- **Nazwy**: Zawiera pola nazewnictwa wymagane w różnych systemach operacyjnych.
- **Strategie nazewnictwa rodzinnego**: FontLab zarządza złożonym schematem nazewnictwa wymaganym przez starsze i nowoczesne platformy. Nazwisko rodziny służy jako nadrzędny identyfikator, podczas gdy nazwy stylów różnicują warianty. Najlepsza praktyka nakazuje skonfigurowanie zarówno _Preferowanej Rodziny_ (pozwalającej na nieograniczoną wagę/stylów), jak i _Rodziny Map Stylów_ (ograniczającej grupy stylów do standardowej struktury RIBBI z czterema stylami: Regularny, Kursywa, Pogrubiona, Pogrubiona Kursywa) w celu uzyskania maksymalnej kompatybilności.
- **Stylizacja i klasyfikacja**: W _Klasyfikacji_ użytkownicy mogą zdefiniować klasę wagową, klasę szerokości i nachylenie każdego wzorca. Dodatkowo parametry **PANOSE** umożliwiają określenie deskryptorów liczbowych dla takich cech, jak styl szeryfowy, proporcje, kontrast i zachowanie linii środkowej. Wartości te pomagają systemom operacyjnym w zastępowaniu brakujących czcionek wizualnie podobnymi projektami.
- **Metryki i parametry**: Metryki globalne — w tym wzniesienie, zejście, wysokość nasadki, wysokość x i strefy wyrównania — są definiowane dla każdego elementu głównego. Wartości te wyznaczają metryki pionowe i wpływają na zachowanie automatycznych podpowiedzi.> [!WAŻNE] Niespójne nazewnictwo rodzin lub źle skonfigurowane mapowanie stylów RIBBI może prowadzić do konfliktów instalacyjnych, błędów łączenia stylów między platformami i nieprawidłowego renderowania w edytorach tekstu.

## Konfigurowanie osi zmienności

Podczas projektowania czcionki zmiennej lub rodziny z wieloma wzorcami podstawowym krokiem jest zdefiniowanie osi przestrzeni projektowej. Oś reprezentuje kierunek zmienności, taki jak waga, szerokość lub osie projektu niestandardowego.

- **Standardowe osie**: Zwykle używaj standardowych czteroliterowych znaczników zdefiniowanych w specyfikacji OpenType, takich jak „wght” (waga) i „wdth” (szerokość).
- **Niestandardowe osie**: Możesz tworzyć niestandardowe osie, używając znaczników wielkich liter (np. `GRAD` dla oceny, `SERF` dla rozmiaru szeryfowego).

Każda oś wymaga znacznika, nazwy i zdefiniowanego zakresu. Każdy mistrz jest umieszczany na określonym skrzyżowaniu współrzędnych.

> [!UWAGA] Każdy główny glif musi mieć dokładnie tę samą liczbę konturów, węzłów, uchwytów i punktów początkowych, aby zapewnić zgodność interpolacji. Zmiana ciągłości węzła (np. ciągłości krzywizny G2) lub zmiana kierunku konturu pomiędzy wzorcami spowoduje przerwanie interpolacji.

## Mapowanie wykresu osiJedną z najpotężniejszych funkcji silnika odmian FontLab 7 jest **Axis Graph**, który odwzorowuje współrzędne przestrzeni projektowej na współrzędne użytkownika.

1. **Współrzędne przestrzeni projektowej**: Surowe, wewnętrzne wartości używane podczas rysowania (np. pomiary grubości pnia, takie jak 40 do 180 jednostek, które bezpośrednio określają rozmieszczenie węzłów krzywej Beziera i szerokość postępu).
2. **Współrzędne użytkownika**: Wartości zewnętrzne udostępniane użytkownikom końcowym (np. skala wag CSS od 100 do 900).

Wykres osi definiuje mapowanie pomiędzy tymi dwiema przestrzeniami. Domyślnie to mapowanie jest liniowe. Jednakże wizualny postęp masy ciała rzadko jest liniowy; skok z Light (300) na Regular (400) wymaga innego fizycznego zwiększenia szerokości mostka i łożysk bocznych niż z Bold (700) na Black (900).

> [!WSKAZÓWKA] Użyj wykresu osi, aby utworzyć mapowanie nieliniowe. Zapewnia to płynną interpolację suwaków skierowanych do użytkownika i tworzenie wizualnie zrównoważonych przejść, nawet jeśli przesunięcia współrzędnych krzywej Beziera są nieliniowe.

---

# Rozdział 18: Zmienne czcionki i zgodność konturówW FontLab 7 proces pracy z wieloma wzorcami i osiami projektowymi w celu uzyskania dynamicznych instancji nazywany jest wariacją. Tworzenie czcionki zmiennej wymaga skonfigurowania przestrzeni projektowej i upewnienia się, że kontury główne są w pełni kompatybilne z interpolacją.

## Projektowanie przestrzeni projektowej

Przestrzeń projektowa jest definiowana przez jedną lub więcej osi odmian — takich jak waga („wght”), szerokość („wdth”) lub nachylenie („slnt”) — skonfigurowanych w **Informacje o czcionce > Osie**. Wzorce czcionek i wzorce bez czcionek (zdefiniowane na poziomie glifów przy użyciu nazw przyrostków lokalizacji osi, takich jak `:wt=350,wd=75`) są odwzorowywane na określone współrzędne w tej wielowymiarowej przestrzeni projektowej. FontLab 7 wykorzystuje te współrzędne do obliczania interpolacji i ekstrapolacji instancji pośrednich.

> [!WAŻNE] Upewnij się, że wszystkie style główne mają unikalne lokalizacje w przestrzeni projektowej. Nie będziesz mógł poprawnie wyeksportować czcionki ani podglądu odmian, jeśli dwóch wzorców ma identyczne współrzędne.

## Zarys zasad zgodności

Aby interpolacja była płynna, geometria konturu każdego glifu musi idealnie pasować do wszystkich aktywnych wzorców. Kontury są kompatybilne, jeśli spełniają następujące wymagania konstrukcyjne:1. ** Liczba dopasowań**: Glif musi mieć tę samą liczbę elementów i konturów, a każdy kontur musi zawierać dokładnie tę samą liczbę węzłów (zarówno ostrych, jak i gładkich) oraz punktów kontrolnych krzywej Béziera.
2. **Pasujące punkty początkowe**: Wyznaczony punkt początkowy (indeks węzła 0) każdego konturu musi znajdować się w tej samej względnej pozycji topologicznej we wszystkich masterach. Jeśli punkty początkowe nie pokrywają się, kontur będzie się skręcał lub przecinał podczas interpolacji.
3. **Stały kierunek konturu**: Kontury muszą przebiegać w tym samym kierunku (zgodnie z ruchem wskazówek zegara dla liczników lub przeciwnie do ruchu wskazówek zegara dla ścieżek zewnętrznych) we wszystkich wzorcach. Niespójny kierunek powoduje artefakty renderowania i wypełnienia.

> [!TIP] Włącz opcję **Edytuj > Dopasuj podczas edycji**, aby zsynchronizować dodawanie, usuwanie i dostosowywanie węzłów jednocześnie we wszystkich kompatybilnych wzorcach, zachowując zgodność konturów podczas procesu rysowania.

## Diagnozowanie i rozwiązywanie niezgodności

FontLab 7 udostępnia kilka wyspecjalizowanych interfejsów umożliwiających sprawdzenie zgodności konturów przed eksportem:- **Niepasujący filtr paska bocznego**: W oknie Czcionka rozwiń sekcję **Warstwy i wzorce** na pasku bocznym. Filtr **Niepasujące** wyświetla dokładną liczbę niezgodnych glifów. Kliknięcie tego filtra izoluje te glify w celu szybkiego rozwiązywania problemów.
- **Narzędzie swatające**: Aktywuj to narzędzie, naciskając klawisz „7”. Na pasku właściwości wyświetlany jest zielony wskaźnik stanu, jeśli urządzenia główne są kompatybilne, i czerwony, jeśli nie są. Matchmaker pokazuje numery węzłów i kody kolorów pasujące do konturów. Możesz wybrać odpowiednie zakresy węzłów i pozwolić systemowi losowania automatycznie zharmonizować segmenty ścieżki.
- **Podgląd interpolacji**: Użyj panelu **Odmiany**, aby poruszać się po przestrzeni projektowej. Rysując wektor interpolacji w widoku mapy, możesz sprawdzić podgląd **Interpolacji** w panelu Podgląd, aby sprawdzić kroki pośrednie.

## Eksport zmiennej czcionki

Po sprawdzeniu zgodności wybierz **Plik > Eksportuj czcionkę jako** i wybierz format zmienny, np. **Zmienny TT (.ttf)** lub **Zmienny PS (.otf)**. FontLab kompiluje parametry przestrzeni projektowej, domyślne struktury główne i delty interpolacyjne do ostatecznej czcionki OpenType Variations.

---# Rozdział 19: Skrypty i automatyzacja w Pythonie

FontLab 7 zawiera wbudowane, wieloplatformowe środowisko skryptowe Python 3, które umożliwia projektantom czcionek i inżynierom czcionek automatyzowanie powtarzalnych zadań, wykonywanie modyfikacji wsadowych i rozszerzanie interfejsu aplikacji. Wchodząc w interakcję z wewnętrznymi strukturami danych FontLab, skrypty mogą programowo manipulować krzywymi Beziera, dostosowywać poziome nawiązania boczne i szerokości postępów, zarządzać funkcjami układu OpenType i konstruować niestandardowe przepływy pracy.

## Panel skryptowy i środowisko

Podstawowym interfejsem do wykonywania kodu skryptu jest **panel Skrypty** (_Okno > Panele > Skrypty_). Panel zawiera prosty edytor kodu z podświetlaniem składni, konsolę wyjściową wyświetlającą wyniki lub błędy wykonania oraz elementy sterujące umożliwiające uruchamianie skryptów. Użytkownicy mogą pisać kod bezpośrednio w edytorze, ładować zewnętrzne skrypty `.py` lub interaktywnie uruchamiać poszczególne instrukcje.

Dodatkowo skrypty zapisane w folderze `Skrypty` użytkownika są automatycznie rejestrowane w menu _Narzędzia > Skrypty_, co pozwala na przypisanie im niestandardowych skrótów klawiaturowych.

## Wysoki poziom API `fontlab`Pakiet `fontlab` to nowoczesny, wysokopoziomowy interfejs API języka Python przeznaczony do intuicyjnej edycji czcionek i glifów. Działa jako opakowanie aktywnego obszaru roboczego, udostępniając obiekty wysokiego poziomu do wysyłania zapytań i modyfikowania bieżącego stanu projektu:

- **Bieżący obszar roboczy:** Klasa `flWorkspace` obsługuje zarządzanie na poziomie okna. Uzyskaj dostęp do aktywnego obszaru roboczego za pomocą `fontlab.flWorkspace()`.
- **Bieżąca czcionka (pakiet):** Funkcja `CurrentFont()` zwraca aktywną czcionkę jako obiekt `flPackage`. Za pośrednictwem tego obiektu można uzyskać dostęp do globalnych właściwości czcionki, wzorców, metadanych informacji o czcionce, klas i kolekcji glifów czcionki.
- **Wybrane glify:** Funkcja `CurrentGlyph()` zwraca aktywny obiekt `flGlyph` aktualnie otwarty w oknie glifów, natomiast `CurrentFont().selectedGlyphs` zwraca listę wszystkich wybranych glifów w oknie czcionek. Można programowo przeglądać te glify, aby modyfikować węzły konturu, przesuwać łożyska boczne lub wstawiać kotwice.

> [!WSKAZÓWKA] Podczas programowego modyfikowania konturów glifów pracuj ze współrzędnymi zmiennoprzecinkowymi, aby zachować precyzję krzywej Beziera i ciągłość węzła G2 pomiędzy wzorcami. Zaokrąglania liczb całkowitych używaj tylko przed ostatecznym eksportem czcionki.## Interfejsy API niskiego poziomu i starsze wersje: `fontgate` i `FL`

Aby zapewnić głęboką kontrolę nad podstawowym silnikiem aplikacji i zgodnością starszych skryptów, FontLab 7 udostępnia dwa dodatkowe pakiety:

- **Pakiet `fontgate`:** Ta niskopoziomowa biblioteka w języku C++ zawiera surowe struktury danych podstawowego silnika FontLab. Zajmuje się podstawowymi klasami geometrii i serializacji, takimi jak `fgFont`, `fgGlyph`, `fgContour` i `fgPoint`. Choć bardziej skomplikowany w zapisie, oferuje wysoką wydajność przetwarzania podczas wykonywania intensywnych operacji na tysiącach węzłów lub współrzędnych.
- **Pakiet `FL`:** Aby zapewnić kompatybilność wsteczną, FontLab 7 zawiera starsze API `FL`. Symuluje to interfejs skryptowy Python 2 w FontLab Studio 5. Użycie `FL` umożliwia programistom uruchamianie starszych skryptów z minimalnymi modyfikacjami, ułatwiając przejście do nowoczesnego API Python 3.

## Niestandardowe interfejsy użytkownika z PythonQt

Dzięki integracji **PythonQt** skrypty mogą uzyskiwać dostęp do bazowego frameworku Qt w celu tworzenia bogatych, natywnych interfejsów użytkownika.Zamiast działać po cichu lub polegać na prostych podpowiedziach wiersza poleceń, programiści mogą importować moduły z `PythonQt.QtGui` i `PythonQt.QtCore` w celu tworzenia niestandardowych okien dialogowych, wprowadzania tekstu, przycisków i paneli ustawień. Te niestandardowe okna dziedziczą styl FontLab i działają w głównej pętli aplikacji.

> [!WAŻNE] Tworząc niestandardowe okna interfejsu użytkownika przy użyciu PythonQt, zawsze upewnij się, że okna dialogowe są odpowiednio powiązane z głównym oknem FontLab, aby zapobiec problemom z blokowaniem fokusu lub awariom aplikacji po zakończeniu działania skryptu.

---

# Rozdział 20: Testowanie, sprawdzanie i eksportowanie

Przed wypuszczeniem czcionki niezbędny jest systematyczny przepływ pracy obejmujący kontrolę jakości, kontrolę konspektu i weryfikację kompilacji. FontLab 7 zapewnia wbudowane narzędzia umożliwiające podgląd zachowania układu, diagnozowanie błędów konturów, konfigurowanie technicznych profili eksportu i pakowanie końcowych czcionek statycznych lub zmiennych.

## Kontrola jakości i sprawdzanie wizualneTesty wizualne rozpoczynają się w **panelu podglądu**, działającej piaskownicy umożliwiającej renderowanie, odstępy i funkcje OpenType. W przeciwieństwie do standardowego okna Glifów, panel Podgląd umożliwia wpisywanie niestandardowych ciągów tekstowych, testowanie kroków interpolacji między wzorcami i sprawdzanie zachowań renderowania w różnych rozmiarach. Możesz wybrać różne tryby (np. Treść, Odstępy lub Kerning) i wyświetlić podgląd poszczególnych wzorców lub określonych lokalizacji przestrzeni projektowej.

Aby sprawdzić właściwości układu — takie jak ligatury („liga”), kapitaliki („smcp”) lub pozycjonowanie od znaku do podstawy („mark”) — należy najpierw skompilować kod funkcji OpenType. Otwórz **panel Funkcje** i kliknij przycisk **Kompiluj**. Po skompilowaniu funkcje te można włączać i wyłączać bezpośrednio w panelu Podgląd lub na pasku narzędzi tekstowych, aby mieć pewność, że reguły podstawiania i pozycjonowania działają zgodnie z przeznaczeniem.

> [!UWAGA] Jeśli Twoja rodzina czcionek zawiera wiele wzorców i ręcznie zdefiniowałeś swoje funkcje, upewnij się, że Twoje profile eksportu są skonfigurowane tak, aby tworzyć funkcje dla każdego wzorca oddzielnie. Zapobiega to zastąpieniu przez zduplikowane definicje obiektów unikalnych metryk głównych.

## Automatyczne audyty za pomocą FontAudit**FontAudit** firmy FontLab to zautomatyzowany silnik, który analizuje kontury glifów pod kątem błędów technicznych. Możesz go aktywować poprzez `Widok > Pokaż > FontAudit` lub otworzyć panel FontAudit (`Okno > Panele > FontAudit`), aby sprawdzić bieżącą warstwę. Aby sprawdzić wiele glifów, zaznacz je w oknie Czcionka i wybierz `Glif > Glify FontAudit`. Czerwone flagi w narożnikach wskazują rozwiązane i nierozwiązane problemy, które można naprawić globalnie za pomocą `Glyph > Napraw problemy FontAudit` lub indywidualnie w panelu. Kluczowe kontrole obejmują:

- **Przecięcia:** nakładające się kontury, które mogą powodować artefakty rasteryzacji.
- **Brakujące ekstrema:** Segmenty krzywej pozbawione węzłów w najbardziej zewnętrznych punktach pionowych lub poziomych. Węzły ekstremów są kluczowe dla rozmieszczenia wskazówek i spójności interpolacji.
- **Curve Flats:** Zakrzywione segmenty Beziera z dopasowanymi uchwytami, które można bezstratnie uprościć do linii prostych.
- **Nieregularne i rzadkie pnie:** Niespójności w grubości pnia w porównaniu do typowych wartości ustawionych w `Informacje o czcionce > Pnie`.

## Eksportuj konfigurację profiluEksportowanie przekształca pliki źródłowe programowania (`.vfc`/`.vfj`) w formaty gotowe do produkcji za pomocą okna dialogowego **Eksportuj profile** (`Plik > Eksportuj profile...`). Profile definiują sposób, w jaki FontLab przetwarza kontury, obsługuje nazwy glifów i kompiluje tabele OpenType na wyjściu.

Możesz dostosować profile, aby kontrolować precyzję współrzędnych. Kontury TrueType (`.ttf`) wymagają zaokrąglenia współrzędnych do liczb całkowitych, podczas gdy kontury PostScriptu (`.otf`) obsługują współrzędne ułamkowe, aby zachować wierność krzywej Beziera kosztem nieco większych rozmiarów plików. Profile decydują także o usuwaniu zapętlonych rogów, konwertowaniu nazw glifów programistycznych na nazwy produkcyjne i generowaniu funkcji kerningu OpenType lub znacznika do znacznika („mkmk”).

## Kompilowanie i pakowanie

Aby wygenerować ostateczne czcionki, wybierz `Plik > Eksportuj czcionkę jako...`.

- **Statyczny OTF/TTF:** Wybierz standardowe profile OpenType PS (`.otf`) lub OpenType TT (`.ttf`).
- **Czcionki zmienne:** Użyj profilu **Zmienna TT (.ttf)**. W przypadku pakowania zmiennych wszystkie wzorce muszą zachować kompatybilność węzłów — co oznacza identyczne kierunki konturów, zgodną liczbę węzłów i identyczne punkty początkowe.