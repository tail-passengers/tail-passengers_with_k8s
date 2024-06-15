import { getCurrentLanguage, changeLanguage } from "../utils/languageUtils.js";
import locales from "../utils/locales/locales.js";

export function renderFooterSection() {
  const footerContainer = document.querySelector("#footer");
  footerContainer.innerHTML = renderFooter();
}

export default function renderFooter() {
  return `
		<footer class="tp-footer-container tp-bgc-secondary tp-color-primary">
			<div class="p-4">
				<div class="column">
					<div class="row">
						<div class="h2 col">
							Tail Passenger
						</div>
						<div class="h5 col default-container">
							© 2024.4.19 Tail Passenger
						</div>
					</div>
					<div class="row">
						<div class="h5 col">
							All rights reserved.
						</div>
					</div>
					
				</div>
			</div>
		</footer>
  `;
}
